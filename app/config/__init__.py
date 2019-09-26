import os

env = os.getenv('ENV', 'dev')

if env == 'dev':
    from .dev_config import Configuration