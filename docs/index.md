FastAPI-AuthControl
===================
Authentication running on FastAPI-Users

Installation
------------

Installation is a 2-step process. First you install the package then install the fork it depends on.

### Install with `pip`

```bash
pipenv install fastapi-authcontrol
```

### Install the fork of FastAPI-Users

```bash
pipenv install -e git+git://github.com/dropkickdev/fastapi-users.git@master#egg=fastapi-users
```

!!! note
    Until there is a way to include a fork in the *install_requires* section of its dependencies,
     the fork will have to be installed manually.

Features
--------
Authcontrol is a custom implementation of the [fastapi-users](https://frankie567.github.io/fastapi-users/) package for [FastAPI](https://fastapi.tiangolo.com/). Authcontrol implements the following:

- JWT Authentication
- Registration routes
- Login/out routes
- Access token routes w/ autorefresh as needed


Documentation
-------------
View the documentation at: https://dropkickdev.github.io/fastapi-authcontrol/


Changelog
----------
To follow
