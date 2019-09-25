from app import app
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    taskBase = celery.Task

    class ContextTask(taskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def sample_task(arg1):
    print("inside task:{0}".format(arg1))

