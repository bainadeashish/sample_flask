from flask_restful import Resource
from flask import jsonify
from flask_restful import reqparse
from app.tasks import sample_task, celery
from flask_restplus import inputs
import time


class sample(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('start_date', required=True, location='args', type=inputs.datetime_from_iso8601,
                                   help="Enter date in YYYY-MM-DD format Or Invalid Date ")
        self.reqparse.add_argument('end_date', required=True, location='args', type=inputs.datetime_from_iso8601,
                                   help="Enter date in YYYY-MM-DD format Or Invalid Date")
        super(sample, self).__init__()

    def post(self):
        '''
        This date start & end date as input.
        It will call a celery task which will combine all the files in between start & end date.
        It will reorder the merge file based on timestamp column & upload file to S3 Server.
        :return:
        The Merged file name which gets uploaded to S3
        '''
        args = self.reqparse.parse_args()
        epoch = time.time()
        # sample_task(args['start_date'], args['end_date'], epoch)
        celery.send_task('app.tasks.sample_task', [args['start_date'], args['end_date'], epoch])
        return jsonify(file_name_formation='Concat of start date,end date & epoch to generate unique filename',
                       http_status_code=200, msg='File merged & can be found with name {0}_{1}_{2}.csv'.format(args['start_date'],
                                                                                                               args['end_date'], epoch))

