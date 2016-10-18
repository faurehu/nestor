from nestor.models.audio import Audio
from nestor.models.context import Context
from nestor.models.action import Action
from nestor.config import SECRET_TOKEN
from nestor.helpers import generate_token
from nestor.logger import logger
from nestor.db import db

from flask import Blueprint, request, make_response
from datetime import datetime
import json

from werkzeug.exceptions import BadRequest
from nestor.errors import InvalidAttribute, RouteException

routes = Blueprint('routes', __name__)

HTTP_OK = 200
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_BAD_REQUEST = 400

def check_token(payload):
    if payload[0].get('token', '') != SECRET_TOKEN:
        raise RouteException('token is invalid', HTTP_BAD_REQUEST)

def handle_cookies():
    cookies = request.cookies
    nestor_token = cookies.get('nestor_token', None)

    if not nestor_token:
        nestor_token = generate_token(10)

    return nestor_token

@routes.route('/ping', methods=['GET'])
def ping():
    return json.dumps({'ping': True})

@routes.route('/', methods=['GET'])
@routes.route('/stories', methods=['GET'])
def stories():
    # TODO: This will eventually need paging
    json_request = request.args.get('json', False)
    status_code = HTTP_OK
    response = {'ok': True}

    nestor_token = handle_cookies()

    stories = Audio.get_stories()

    if json_request:
        response['data'] = {
            'stories': [x.serialize() for x in stories]
        }

    response_obj = make_response(json.dumps(response))
    response_obj.set_cookie('nestor_token', nestor_token)
    return response_obj, status_code

# @routes.route('/ad', methods=['GET'])
# def ad():
#     response = {'ok': True}
#     return response, HTTP_OK

# @routes.route('/story/<id>', methods=['GET'])
# def story(id):
#     json_request = request.args.get('json', False)
#     status_code = HTTP_OK
#     response = {'ok': True}

#     try:
#         story = Audio.get_story(id)
#         if story is None:
#             # Return 404
#             raise Exception('not found')

#         if json_request:
#             response['data'] = {
#                 'story': story.serialize()
#             }

#     except Exception as e:
#         print(e)
#         response = {'ok': False}
#         status_code = HTTP_INTERNAL_SERVER_ERROR

#     return json.dumps(response), status_code

@routes.route('/action', methods=['POST'])
def action():
    status_code = HTTP_OK
    response = {'ok': True}

    cookie = handle_cookies()

    try:
        payload = request.get_json(force=True)
    except BadRequest:
        raise RouteException('payload is not a valid json', HTTP_BAD_REQUEST)

    if not isinstance(payload, list):
        payload = [payload]

    if not payload:
        raise RouteException('payload is an empty list', HTTP_BAD_REQUEST)

    check_token(payload)

    response['action_id'] = []

    for obj in payload:
        try:
            action = Action(None, cookie, obj['audio_id'], obj['type'], obj['audio_point'], datetime.utcnow())
        except InvalidAttribute as e:
            raise RouteException(str(e), HTTP_BAD_REQUEST)
        db.session.add(action)
        response['action_id'].append(action.id)

    if len(response['action_id']) == 1:
        response['action_id'] = response['action_id'][0]

    try:
        db.session.commit()
    except Exception as e:
        logger.error(e)
        raise RouteException('something went wrong storing the data', HTTP_SERVER_ERROR)

    response_obj = make_response(json.dumps(response))
    #TODO: Check if should be reset only if necessary
    response_obj.set_cookie('nestor_token', cookie)
    return response_obj, status_code

@routes.route('/context', methods=['POST'])
def context():
    status_code = HTTP_OK
    response = {'ok': True}

    try:
        payload = request.get_json(force=True)
    except BadRequest:
        raise RouteException('payload is not a valid json', HTTP_BAD_REQUEST)

    if not isinstance(payload, list):
        payload = [payload]

    if not payload:
        raise RouteException('payload is an empty list', HTTP_BAD_REQUEST)

    check_token(payload)

    for obj in payload:
        type = obj.get('type', None)
        audio_id = obj.get('audio_id', None)
        time_start = obj.get('time_start', None)
        time_end = obj.get('time_end', None)
        link_uri = obj.get('link_uri', None)
        img_uri = obj.get('img_uri', None)
        text = obj.get('text', None)

        try:
            context = Context(type, audio_id, time_start, time_end, link_uri, img_uri, text)
        except (InvalidAttribute, MissingAttribute) as e:
            raise RouteException(str(e), HTTP_BAD_REQUEST)
        db.session.add(context)

    try:
        db.session.commit()
    except Exception as e:
        logger.error(e)
        raise RouteException('something went wrong storing the data', HTTP_SERVER_ERROR)

    response_obj = make_response(json.dumps(response))
    return response_obj, status_code

@routes.route('/audio', methods=['POST'])
def audio():
    status_code = HTTP_OK
    response = {'ok': True}

    try:
        payload = request.get_json(force=True)
    except BadRequest:
        raise RouteException('payload is not a valid json', HTTP_BAD_REQUEST)

    if not isinstance(payload, list):
        payload = [payload]

    if not payload:
        raise RouteException('payload is an empty list', HTTP_BAD_REQUEST)

    check_token(payload)

    response['audio_id'] = []

    for obj in payload:
        title = obj.get('title', '')
        type = obj.get('type', '')
        author = obj.get('author', '')
        description = obj.get('description', '')
        audio_uri = obj.get('audio_uri', '')
        link_uri = obj.get('link_uri', '')

    try:
        audio = Audio(None, title, type, author, description, link_uri, audio_uri)
    except InvalidAttribute as e:
        raise RouteException(e.unpack())
    db.session.add(audio)
    response['audio_id'].append(audio.id)

    if len(response['audio_id']) == 1:
        response['audio_id'] = response['audio_id'][0]

    try:
        db.session.commit()
    except Exception as e:
        logger.error(e)
        raise RouteException('something went wrong storing the data', HTTP_SERVER_ERROR)

    return json.dumps(response), status_code
