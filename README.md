# generate all log files
step 1
python log-generator.py --path local_path --days 5 --lines 500 --files 3

Note: Change the ENV variable in config to dev if you have system other than macOS.

# Run Docker-compose from path where docker-compose.yml exists
docker-compose up -d

This will start up below processes
a.Rabbitmq
b.Flower
c.minio
d.backend flask application


# upload the log files which generated previously (step 1 at path local_path) by logging into minio server
http://127.0.0.1:9000

Username: password present in docker-compose.yml
    environment:
      MINIO_ACCESS_KEY: minio
      MINIO_SECRET_KEY: minio123

# POST method API which accepts the date range & return a file name in response

http://0.0.0.0:5000/api/v1/sample?start_date=2019-09-21&end_date=2019-09-24

Calling this endpoint should initiate the merging of files contained in the S3
bucket as a background task in celery.
The endpoint should return a filename, by which we can download through minio server
the single merged and sorted file, with the contents of all the files with
names within the given date range.
