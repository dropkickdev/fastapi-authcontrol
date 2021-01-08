from fastapi_users import FastAPIUsers, models
from fastapi_users.db import TortoiseUserDatabase, TortoiseBaseUserModel
from fastapi_users.authentication import JWTAuthentication
from limeutils import classgrabber

from . import AuthSettings


class Authcontrol:
    s: AuthSettings
    debug: bool = False
    
    def __init__(self, settings: AuthSettings):
        self.s = settings
        UserTbl: TortoiseBaseUserModel = classgrabber(settings.USER_TABLE)
        User: models.BaseUser = classgrabber(settings.USER_MODEL)
        UserCreate: models.BaseUserCreate = classgrabber(settings.USERCREATE_MODEL)
        UserUpdate: models.BaseUserUpdate = classgrabber(settings.USERUPDATE_MODEL)
        UserDB: models.BaseUserDB = classgrabber(settings.USERDB_MODEL)
        
        self.jwt = JWTAuthentication(secret=settings.SECRET_KEY,
                                     lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE)
        
        self.user_db = TortoiseUserDatabase(UserDB, UserTbl)    # noqa
        self.fapi_user = FastAPIUsers(self.user_db, [self.jwt], User, UserCreate,   # noqa
                                      UserUpdate, UserDB)   # noqa
    
