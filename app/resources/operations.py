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

    def get(self):
        args = self.reqparse.parse_args()
        epoch = time.time()
        # sample_task(args['start_date'], args['end_date'], epoch)
        celery.send_task('app.tasks.sample_task', [args['start_date'], args['end_date'], epoch])
        return jsonify(http_status_code=200, msg='File merged & can be found with name {0}_{1}_{2}.csv'.format(args['start_date'],
                                                                                                               args['end_date'], epoch))
