import secrets, pytz
from datetime import datetime, timedelta
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import TortoiseUserDatabase, TortoiseBaseUserModel
from fastapi_users.authentication import JWTAuthentication
from limeutils import classgrabber

from .models import Token
from . import AuthSettings


class Authcontrol:
    s: AuthSettings
    debug: bool = False
    # UserTable: TortoiseBaseUserModel
    # User: models.BaseUser
    # UserCreate: models.BaseUserCreate
    # UserUpdate: models.BaseUserUpdate
    # UserDB: models.BaseUserDB
    
    
    def __init__(self, settings: AuthSettings):
        self.s = settings
        self.UserTable: TortoiseBaseUserModel = classgrabber(settings.USER_TABLE)
        self.User: models.BaseUser = classgrabber(settings.USER_MODEL)
        self.UserCreate: models.BaseUserCreate = classgrabber(settings.USERCREATE_MODEL)
        self.UserUpdate: models.BaseUserUpdate = classgrabber(settings.USERUPDATE_MODEL)
        self.UserDB: models.BaseUserDB = classgrabber(settings.USERDB_MODEL)
        
        self.jwtauth = JWTAuthentication(secret=settings.SECRET_KEY,
                                         lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE)
        self.user_db = TortoiseUserDatabase(self.UserDB, self.UserTable)    # noqa
        self.fapi_user = FastAPIUsers(self.user_db, [self.jwtauth], self.User,          # noqa
                                      self.UserCreate, self.UserUpdate, self.UserDB)    # noqa

    @staticmethod
    def generate_refresh_token(nbytes: int = 32):
        return secrets.token_hex(nbytes=nbytes)

    @staticmethod
    def _time_difference(expires: datetime, now: datetime = None):
        """Get the diff between 2 dates"""
        now = now or datetime.now(tz=pytz.UTC)
        diff = expires - now
    
        return {
            'days': diff.days,
            'hours': int(diff.total_seconds()) // 3600,
            'minutes': int(diff.total_seconds()) // 60,
            'seconds': int(diff.total_seconds()),
        }

    @classmethod
    def refresh_cookie(cls, name: str, token: dict, **kwargs):
        if token['expires'] <= datetime.now(tz=pytz.UTC):
            raise ValueError('Cookie expires date must be greater than the date now')
    
        expires = token['expires'] - datetime.now(tz=pytz.UTC)
        cookie_data = {
            'key': name,
            'value': token['value'],
            'httponly': True,
            'expires': expires.seconds,
            'path': '/',
            **kwargs,
        }
        # if not s.DEBUG:
        #     cookie_data.update({
        #         'secure': True
        #     })
        return cookie_data

    @classmethod
    def expires(cls, expires: datetime, units: str = 'minutes'):
        diff = cls._time_difference(expires)
        return diff[units]
    
    # TODO: Converted this to an object method instead of a class method so updates are needed
    async def create_refresh_token(self, user) -> dict:
        """
        Create and save a new refresh token
        :param user Pydantic model for the user
        """
        if not isinstance(user, models.BaseUserDB):
            raise TypeError('User must be a valid UserDB.')
        
        user = await self.UserTable.get(pk=user.id).only('id')
        refresh_token = Authcontrol.generate_refresh_token()
        expires = datetime.now(tz=pytz.UTC) + timedelta(seconds=self.s.REFRESH_TOKEN_EXPIRE)
    
        await Token.create(token=refresh_token, expires=expires, author=user)
        return {
            'value': refresh_token,
            'expires': expires,
        }

    # TODO: Converted this to an object method instead of a class method so updates are needed
    async def update_refresh_token(self, user) -> dict:
        """
        Update the refresh token of the user
        :param user Pydantic model for the user
        """
        if not isinstance(user, models.BaseUserDB):
            raise TypeError('User must be a valid UserDB.')
        
        refresh_token = Authcontrol.generate_refresh_token()
        expires = datetime.now(tz=pytz.UTC) + timedelta(seconds=self.s.REFRESH_TOKEN_EXPIRE)
        token = await Token.get(author_id=user.id, is_blacklisted=False).only('id', 'token',
                                                                              'expires')
        token.token = refresh_token
        token.expires = expires
        await token.save(update_fields=['token', 'expires'])
        return {
            'value': refresh_token,
            'expires': expires,
        }