from typing import List
from pydantic import BaseSettings, validator
from fastapi_users import FastAPIUsers
from fastapi_users.db import TortoiseUserDatabase
from fastapi import Request
from fastapi_users.authentication import JWTAuthentication

from . import AuthSettings
from .models import *


class Authcontrol:
    s: AuthSettings
    
    def __init__(self, settings: AuthSettings):
        self.s = settings
        self.auth_jwt = JWTAuthentication(secret=self.s.SECRET_KEY,
                                          lifetime_seconds=self.s.ACCESS_TOKEN_EXPIRE)
        
        self.user_db = TortoiseUserDatabase(UserDB, UserTbl)

        self.fapi_user = FastAPIUsers(self.user_db, [self.auth_jwt], User, UserCreate,
                                      UserUpdate, UserDB)