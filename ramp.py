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
        try: 
            args["message"]
            return True
        except KeyError:
            if args["length_unit"] == 'mm':
                length_temp = args["length"]
            if args["length_unit"] == 'inches':
                length_temp = args["length"]*25.4
            if length_temp > 380.0:
                message = {"message": "length can not be larger than 380mm or 14.9606 inches"}
            else: 
                return False
            return message

def abort_if_exceeds_width_limit(args):
        try: 
            args["message"]
            return True
        except KeyError:
            if args["length_unit"] == 'mm':
                width_temp = args["width"]
            if args["length_unit"] == 'inches':
                width_temp = args["width"]*25.4
            if width_temp > 270.0:
                message = {"message": "width can not be longer than 270mm or 10.6299 inches"}
            else: 
                return False
            return message

def abort_if_exceeds_weight_limit(args):
        try: 
            args["message"]
            return True
        except KeyError:
            if args["weight_unit"] == 'g':
                weight_temp = args["weight"]
            if args["weight_unit"] == 'ounces':
                weight_temp = args["weight"]*28.3495
            if weight_temp > 500.0:
                message = {"message": "weight can not be heavier than 500g or 17.637 ounces"}
            else: 
                return False
            return message

def post_rate_calculation(args, message):
    try:
        args["message"]
        return False
    except KeyError:
        if args["length_unit"] == 'mm':
            length_temp = args["length"]
        elif args["length_unit"] == 'inches':
            length_temp = args["length"]*25.4 
        if args["length_unit"] == 'mm':
            width_temp = args["width"]
        elif args["length_unit"] == 'inches':
            width_temp = args["width"]*25.4
        if args["weight_unit"] == 'g':
            weight_temp = args["weight"]
        elif args["weight_unit"] == 'ounces':
            weight_temp = args["weight"]*28.3495

        # determine if the envelope is standard or not
        if length_temp >=140.0 and length_temp <= 245.0 and width_temp >= 90.0 and width_temp <= 156.0 and weight_temp >= 3.0 and weight_temp <= 50.0: 
            isStandard = True 
        else: 
            isStandard = False
        
        # Postal rate calcualtion: 
        # for a standard envelop
        if isStandard == True: 
        # for a non-standard envelop
         

class Calculator(Resource):
    def put(self):
        args = input_args.parse_args()
        message = abort_if_exceeds_length_limit(args)
        if message != True and message != False: 
            args = message
        message = abort_if_exceeds_width_limit(args)
        if message != False and message != True: 
            args = message
        message = abort_if_exceeds_weight_limit(args)
        if message != False and message != True: 
            args = message
        #print(args)
        return args   

api.add_resource(Calculator,"/calculator")
if __name__ == "__main__":
    app.run(debug=True)