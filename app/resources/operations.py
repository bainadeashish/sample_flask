from flask_restful import Resource
from flask_restful import reqparse
from app.tasks import sample_task, celery


class sample(Resource):
    def get(self):
        celery.send_task('app.tasks.sample_task', ['ashish'])
        return "hello"
