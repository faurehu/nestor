from flask import Blueprint, request
from nestor.models.audio import Audio
from nestor.config import SECRET_TOKEN
import json

from werkzeug.exceptions import BadRequest
from nestor.errors import InvalidAttribute

routes = Blueprint('routes', __name__)

HTTP_OK = 200
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_BAD_REQUEST = 400

@routes.route('/ping', methods=['GET'])
def ping():
    return json.dumps({'ping': True})

@routes.route('/', methods=['GET'])
@routes.route('/stories', methods=['GET'])
def stories():
    json_request = request.args.get('json', False)
    status_code = HTTP_OK
    response = {'ok': True}

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
    response = {'ok': True}
    return response, HTTP_OK

@routes.route('/story/<id>', methods=['GET'])
def story(id):
    json_request = request.args.get('json', False)
    status_code = HTTP_OK
    response = {'ok': True}

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
    resopnse = {'ok': True}
    return response, HTTP_OK

@routes.route('/audio', methods=['POST'])
def audio():
    status_code = HTTP_OK
    response = {'ok': True}

    try:
        # Raises BadRequest
        payload = request.get_json(force=True)

        if not isinstance(payload, list):
            payload = [payload]

        if not payload:
            raise Exception('payload is an empty list')

        if payload[0].get('token', '') != SECRET_TOKEN:
            raise Exception('token is invalid')

        response['audio_id'] = []

        for obj in payload:
            title = obj.get('title', '')
            type = obj.get('type', '')
            author = obj.get('author', '')
            description = obj.get('description', '')
            audio_uri = obj.get('audio_uri', '')
            link_uri = obj.get('link_uri', '')

            # Raises InvalidAttribute
            audio = Audio(None, title, type, author, description, link_uri, audio_uri)
            response['audio_id'].append(audio.id)

        if len(response['audio_id']) == 1:
            response['audio_id'] = response['audio_id'][0]

    except BadRequest:
        response['ok'] = False
        response['error'] = 'payload is not valid json'
    except InvalidAttribute as e:
        response['ok'] = False
        response['error'], status_code = e.unpack()
    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)
        status_code = HTTP_BAD_REQUEST

    return json.dumps(response), status_code
