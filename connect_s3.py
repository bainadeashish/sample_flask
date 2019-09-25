import boto3
from botocore.client import Config
import pandas as pd
from datetime import date, timedelta
bucket_name = 'logs'

s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='minio',
                    aws_secret_access_key='minio123',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')




sdate = date(2019, 9, 21)   # start date
edate = date(2019, 9, 23)   # end date
file_matters = []
delta = edate - sdate       # as timedelta


for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    day = day.strftime('%Y-%m-%d')
    file_matters.append(day)

print("File Matters :{0}".format(str(file_matters)))


# list all the files
appended_df = []
for file_object in s3.Bucket(bucket_name).objects.all():

    if file_object.key[:10] in file_matters:
        print(file_object.key)
        s3.Bucket(bucket_name).download_file(file_object.key, '/data/{0}'.format(file_object.key))
        df = pd.read_csv(r'/data/{0}'.format(file_object.key), header=None, sep=" ", error_bad_lines=False)
        appended_df.append(df)
try:
    concat_df = pd.concat(appended_df)
    concat_df = concat_df.sort_values(by=0)
    concat_df.reset_index()
    concat_df.to_csv('/data/{0}_{1}.csv'.format(sdate, edate), index=False)
    s3.Bucket(bucket_name).upload_file('/data/{0}_{1}.csv'.format(sdate, edate), '{0}_{1}.csv'.format(sdate, edate))

    print("Data for dates between {0} and {1}".format(sdate, edate))
except ValueError:
    print("No Data for dates between {0} and {1}".format(sdate, edate))




