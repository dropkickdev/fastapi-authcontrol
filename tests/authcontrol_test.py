import pytz, pytest
from datetime import datetime, timedelta
from authcontrol import Authcontrol


def test_refresh_cookie():
    name = 'foo'
    now = datetime.now(tz=pytz.UTC)
    token = dict(value='bar')

    cookie_data = {
        'key': 'foo',
        'value': 'bar',
        'httponly': True,
        'path': '/',
    }
    token['expires'] = now + timedelta(minutes=2)
    d = {**cookie_data, 'expires': 119}
    assert Authcontrol.refresh_cookie(name, token) == d
    
    token['expires'] = now + timedelta(hours=1)
    d = {**cookie_data, 'expires': 3599}
    assert Authcontrol.refresh_cookie(name, token) == d
    
    token['expires'] = now + timedelta(days=1)
    d = {**cookie_data, 'expires': 86399}
    assert Authcontrol.refresh_cookie(name, token) == d
    
    with pytest.raises(ValueError):
        token['expires'] = now - timedelta(hours=1)
        Authcontrol.refresh_cookie(name, token)
        token['expires'] = now
        Authcontrol.refresh_cookie(name, token)
        
        
def test_time_diff():
    now = datetime.now(tz=pytz.UTC)
    
    expires = now + timedelta(minutes=2)
    d = dict(days=0,hours=0,minutes=1,seconds=119)
    assert Authcontrol._time_difference(expires) == d
    
    expires = now + timedelta(hours=1)
    d = dict(days=0, hours=0, minutes=59, seconds=3599)
    assert Authcontrol._time_difference(expires) == d

    expires = now + timedelta(hours=2)
    d = dict(days=0, hours=1, minutes=119, seconds=7199)
    assert Authcontrol._time_difference(expires) == d

    expires = now + timedelta(days=2)
    d = dict(days=1, hours=47, minutes=2879, seconds=172799)
    assert Authcontrol._time_difference(expires) == d

    expires = now - timedelta(seconds=60)
    d = dict(days=-1, hours=-1, minutes=-1, seconds=-60)
    assert Authcontrol._time_difference(expires) == d

    expires = now - timedelta(minutes=60)
    d = dict(days=-1, hours=-1, minutes=-60, seconds=-3600)
    assert Authcontrol._time_difference(expires) == d


def test_expires():
    now = datetime.now(tz=pytz.UTC)
    expires = now + timedelta(minutes=2)
    assert Authcontrol.expires(expires) == 1
    assert Authcontrol.expires(expires, 'seconds') == 119

    expires = now + timedelta(days=2)
    assert Authcontrol.expires(expires) == 2879
    assert Authcontrol.expires(expires, 'seconds') == 172799
    assert Authcontrol.expires(expires, 'hours') == 47
    assert Authcontrol.expires(expires, 'days') == 1
