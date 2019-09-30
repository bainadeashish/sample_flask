import os

env = os.getenv('ENV', 'uat')

if env == 'dev':
    from .dev_config import Configuration
elif env == 'uat':
    from .uat_config import Configuration
