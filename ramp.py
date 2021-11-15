from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)

error_message = "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight"

input_args = reqparse.RequestParser()
input_args.add_argument("length_unit", choices = ("mm", "inches"), type=str, help=error_message, required=True)
input_args.add_argument("width", type=float, help=error_message, required=True)
input_args.add_argument("length", type=float, help=error_message, required=True)
input_args.add_argument("weight_unit", choices = ("g", "ounces"), type=str, help=error_message, required=True)
input_args.add_argument("weight", type=float, help=error_message, required=True)

def abort_if_exceeds_length_limit(args):
        if not str.equals(args, "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight"): 
            if str.equal(args["length_unit"], 'mm'):
                length_temp = args["length"]
            if str.equal(args["length_unit"], 'inches'):
                length_temp = args["length"]/25.4
            if length_temp > 380.0:
                abort(406, "length can not be larger than 380mm or 14.9606 inches")

class Calculator(Resource):
    def put(self):
        args = input_args.parse_args()
        #abort_if_exceeds_length_limit(args)
        print(args.json())
        return args   

api.add_resource(Calculator,"/calculator")
if __name__ == "__main__":
    app.run(debug=True)