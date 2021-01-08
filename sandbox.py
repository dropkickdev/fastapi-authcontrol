import importlib
from datetime import datetime
from authcontrol import AuthSettings, Authcontrol, models
from limeutils import classgrabber

# s = AuthSettings(
#     SECRET_KEY='abcaonetuhaoesniuthaosntihaotnsihaosetnuihaoe-sithatsonhui'
# )
# x = classgrabber('authcontrol.models.UserTable')

# ac = Authcontrol(s)
# for i in vars(x):
#     print(i)
#
# print(x)

# instance = x(token='aoeuaoeu', expires=datetime.now())
# # print(type(token), token)
# # print(vars(token))
# for i in instance._meta.db_fields:
#     print(i)