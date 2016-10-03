from flask import Blueprint
import json

routes = Blueprint('routes', __name__)

@routes.route('/ping', methods=['GET'])
def ping():
    return json.dumps({'ping': True})
