from pydantic import BaseSettings, Field


class AuthSettings(BaseSettings):
    # Empty
    SECRET_KEY: str = Field(..., min_length=32)
    
    # Account
    USERNAME_MIN: int = Field(4, ge=4)
    USERNAME_MAX: int = Field(64, le=64)
    PASSWORD_MIN: int = Field(10, ge=10)
    PASSWORD_MAX: int = Field(64, le=64)
    
    # Authentication
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE: int = 60 * 15                  # seconds (15 mins)
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30       # seconds (30 days)
    REFRESH_TOKEN_CUTOFF: int = 30                      # minutes
    REFRESH_TOKEN_KEY = 'refresh_token'
    SESSION_COOKIE_AGE: int = 1209600                   # seconds
    
    # DB tables
    USER_TABLE: str = 'authcontrol.models.UserTable'
    
    # Pydantic models
    USER_MODEL: str = 'authcontrol.models.User'
    USERCREATE_MODEL: str = 'authcontrol.models.UserCreate'
    USERUPDATE_MODEL: str = 'authcontrol.models.UserUpdate'
    USERDB_MODEL: str = 'authcontrol.models.UserDB'
    
    
    class Config:
        case_sensitive = True