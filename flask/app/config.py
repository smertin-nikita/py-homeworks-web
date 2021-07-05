import os

USER_DB = os.getenv('USER_DB')
NAME_DB = os.getenv('NAME_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')

CONFIG = {
    'DEBUG': True,
    'ENV': 'development',
    'POSTGRES_URI': f"postgresql://{USER_DB}:{PASSWORD_DB}@127.0.0.1:5431/{NAME_DB}",
    'SQLALCHEMY_DATABASE_URI': f'postgresql://{USER_DB}:{PASSWORD_DB}@127.0.0.1/{NAME_DB}',
    'SALT': 'my_sJHLHLHKLаваыпuper_s!alt_#4$4344',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JWT_SECRET_KEY': 'jwt-secret-string',

}
