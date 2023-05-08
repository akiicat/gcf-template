import os
from datetime import datetime, timezone, timedelta

from flask import Flask, request
from google.cloud import firestore
import functions_framework
import jsonpickle

if __debug__:
    print("Debug mode")

# get runtime environment
# https://cloud.google.com/functions/docs/configuring/env-var#python_37_and_go_111
project_id = os.environ['GCP_PROJECT']

app = Flask(__name__)
db = firestore.Client(project=project_id)

# Register an HTTP function with the Functions Framework
# Your function is passed a single parameter, (request), which is a Flask Request object.
# https://flask.palletsprojects.com/en/1.0.x/api/#flask.Request
@functions_framework.http
def entrypoint(request):
    # Create a new app context for the app
    internal_ctx = app.test_request_context(
        path=request.full_path, method=request.method
    )

    # Copy the request headers to the app context
    internal_ctx.request = request

    # Activate the context
    internal_ctx.push()

    # Dispatch the request to the internal app and get the result
    return_value = app.full_dispatch_request()

    # Offload the context
    internal_ctx.pop()

    # Return the result of the internal app routing and processing
    return return_value

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello World</h1>", 200

@app.route("/read", methods=["GET"])
def read():
    # get url args: http://xxx/xxx?collection=xxxx&data=123
    arg_coll = request.args.get('collection', default = "default", type = str)
    arg_data = request.args.get('data', default = 0, type = int)

    # query from firestore database
    coll_ref = db.collection(arg_coll)
    coll = coll_ref.where(u'Data', u'>=', arg_query).order_by(u'Time', direction=firestore.Query.ASCENDING)

    arr = []

    for obj in coll.stream():
        obj = obj.to_dict()
        arr.append({
            'Data': obj['Data'],
            'Time': obj['Time'],
            })

    return jsonpickle.encode(arr), 200

@app.route("/write", methods=["POST"])
def write():
    # get url args: http://xxx/xxx?collection=xxxx&data=123
    arg_coll = request.args.get('collection', default = "default", type = str)
    arg_data = request.args.get('data', default = 0, type = int)

    # time with timezone
    tz = timezone(timedelta(hours=0))
    dt = datetime.now(tz)

    doc_ref = db.collection(arg).document(arg_coll)
    doc_ref.set({
        u'Date': arg_data,
        u'Timestamp': dt,
        })

    return "ok", 200

@app.route("/echo/<string:id>", methods=["POST", "GET"])
def echo(id):
    if request.is_json:
        return {"id": id, **request.json}, 200
    return {"id": id}, 200

