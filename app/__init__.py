from flask import Blueprint, Flask
from flask_restful import Api
from flask_cors import CORS


API_VERSION = 1
API_URL_PREFIX = '/api/v%s' % API_VERSION
api_blueprint = Blueprint('api', __name__)


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


api = Api(
    app=api_blueprint,
    prefix = API_URL_PREFIX,
    catch_all_404s=True
)

app.config.update(
    CELERY_BROKER_URL='amqp://rabbitmq:rabbitmq@rabbitmq:5672/',
    CELERY_RESULT_BACKEND='amqp://rabbitmq:rabbitmq@rabbitmq:5672/',
    CELERYBEAT_SCHEDULER='app.tasks.sqlalchemy_scheduler:DatabaseScheduler'
)

from app.resources.operations import sample

api.add_resource(sample, '/sample')
app.register_blueprint(api_blueprint)
api.init_app(app)