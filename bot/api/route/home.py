from http import HTTPStatus
from flask import Blueprint
from ..schema.welcome import WelcomeSchema

home_api = Blueprint('api', __name__)


@home_api.route('/')
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200