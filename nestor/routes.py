from flask import Blueprint, request
from nestor.models.audio import Audio
import json

routes = Blueprint('routes', __name__)

success_response = {'ok': True}

HTTP_OK = 200
HTTP_INTERNAL_SERVER_ERROR = 500

@routes.route('/ping', methods=['GET'])
def ping():
    return json.dumps({'ping': True})

@routes.route('/', methods=['GET'])
@routes.route('/stories', methods=['GET'])
def stories():
    json_request = request.args.get('json', False)
    status_code = HTTP_OK
    response = success_response

    try:
        stories = Audio.get_stories()

        if json_request:
            response['data'] = {
                'stories': [x.serialize() for x in stories]
            }

    except Exception as e:
        response = {'ok': False}
        status_code = HTTP_INTERNAL_SERVER_ERROR

    return json.dumps(response), status_code

@routes.route('/ad', methods=['GET'])
def ad():
    return success_response, HTTP_OK

@routes.route('/story/<id>', methods=['GET'])
def story(id):
    json_request = request.args.get('json', False)
    status_code = HTTP_OK
    response = success_response

    try:
        story = Audio.get_story(id)
        if story is None:
            # Return 404
            raise Exception('not found')

        if json_request:
            response['data'] = {
                'story': story.serialize()
            }

    except Exception as e:
        print(e)
        response = {'ok': False}
        status_code = HTTP_INTERNAL_SERVER_ERROR

    return json.dumps(response), status_code

@routes.route('/action', methods=['POST'])
def action():
    return success_response, HTTP_OK

@routes.route('/audio', methods=['POST'])
def audio():
    return success_response, HTTP_OK
