from setuptools import setup

setup(
    name='code-base',
    version='0.0.1',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'aiohttp==3.9.1',
        'aiohttp-apispec==2.2.3',
        'aiohttp-autoreload==0.0.1',
        'aiohttp-middlewares==2.2.1',
        'aiosignal==1.3.1',
        'apispec==3.3.2',
        'astroid==3.0.2',
        'async-timeout==4.0.3',
        'asyncpg==0.29.0',
        'attrs==23.2.0',
        'black==23.12.1',
        'click==8.1.7',
        'coverage==7.4.0',
        'dill==0.3.7',
        'flake8==7.0.0',
        'frozenlist==1.4.1',
        'greenlet==3.0.3',
        'gunicorn==21.2.0',
        'idna==3.6',
        'iniconfig==2.0.0',
        'isort==5.13.2',
        'Jinja2==3.1.3',
        'MarkupSafe==2.1.4',
        'marshmallow==3.20.2',
        'marshmallow-sqlalchemy==0.30.0',
        'mccabe==0.7.0',
        'mkdir==2020.12.3',
        'multidict==6.0.4',
        'mypy-extensions==1.0.0',
        'orderdict==2020.12.3',
        'packaging==23.2',
        'pathspec==0.12.1',
        'platformdirs==4.1.0',
        'pluggy==1.3.0',
        'pycodestyle==2.11.1',
        'pyflakes==3.2.0',
        'pylint==3.0.3',
        'pytest==7.4.4',
        'pytest-cov==4.1.0',
        'python-dotenv==1.0.0',
        'setupcfg==2020.12.3',
        'SQLAlchemy==2.0.25',
        'tomlkit==0.12.3',
        'typing_extensions==4.9.0',
        'values==2020.12.3',
        'webargs==5.5.3',
        'write==2020.12.3',
        'yarl==1.9.4',
    ],
)
