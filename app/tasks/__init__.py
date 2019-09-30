from app import app
from celery import Celery
import boto3
from botocore.client import Config
import pandas as pd
from datetime import date, timedelta
from app.config import Configuration
from datetime import datetime


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
def sample_task(start_date, end_date, epoch):
    print("inside task:{0}".format(start_date))
    sdate = start_date  # start date
    edate = end_date  # end date
    bucket_name = Configuration.bucket_name
    epoch = str(epoch)

    s3 = boto3.resource('s3',
                        endpoint_url=Configuration.endpoint_url,
                        aws_access_key_id=Configuration.aws_access_key_id,
                        aws_secret_access_key=Configuration.aws_secret_access_key,
                        config=Config(signature_version='s3v4'),
                        region_name=Configuration.region_name)

    sdate = datetime.strptime(start_date[:10], '%Y-%m-%d')  # start date
    edate = datetime.strptime(end_date[:10], '%Y-%m-%d')  # end date
    file_matters = []
    delta = edate - sdate  # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        day = day.strftime('%Y-%m-%d')
        file_matters.append(day)

    print("File Matters :{0}".format(str(file_matters)))

    # list all the files
    appended_df = []
    for file_object in s3.Bucket(bucket_name).objects.all():

        if file_object.key[:10] in file_matters and 'log' in file_object.key:
            print(file_object.key)
            s3.Bucket(bucket_name).download_file(file_object.key, '/data/{0}'.format(file_object.key))
            df = pd.read_csv(r'/data/{0}'.format(file_object.key), header=None, sep=" ", error_bad_lines=False)
            appended_df.append(df)
    try:
        concat_df = pd.concat(appended_df)
        concat_df = concat_df.sort_values(by=0)
        concat_df.reset_index()
        concat_df.to_csv('/data/{0}_{1}_{2}.csv'.format(sdate, edate, epoch), index=False)
        s3.Bucket(bucket_name).upload_file('/data/{0}_{1}_{2}.csv'.format(sdate, edate, epoch), '{0}_{1}_{2}.csv'.format(sdate, edate, epoch))

        print("Data for dates between {0} and {1}".format(sdate, edate))
    except ValueError:
        print("No Data for dates between {0} and {1}".format(sdate, edate))

