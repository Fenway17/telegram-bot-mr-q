from flask_marshmallow import Schema
from marshmallow.fields import Str


class WelcomeSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["title", "message"]

    message = Str()