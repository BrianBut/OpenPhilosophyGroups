from flask import Blueprint
from flask_muck import FlaskMuckApiView
import marshmallow as ma
from marshmallow import fields as mf
from app import db
from ..models import Info

class InfoSchema(ma.Schema):
    id = mf.Integer(required=True, dump_only=True)
    text = mf.String(required=True)

class BaseApiView(FlaskMuckApiView):
    """Base view to inherit from. Helpful for setting class variables shared with all API views such as "session"
    and "decorators".
    """
    allowed_methods = {"GET"}
    session = db.session


class TopicInfoApiView(BaseApiView):
    """ToDo API view that provides all RESTful CRUD operations."""

    api_name = "topicinfo"
    Model = Info
    ResponseSchema = InfoSchema
    #CreateSchema = TodoSchema
    #PatchSchema = TodoSchema
    #UpdateSchema = TodoSchema
    searchable_columns = [Info.title]

# This is the existing api blueprint where all other routes are registered.
api = Blueprint("v1_api", __name__, url_prefix="/api")

TopicInfoApiView.add_rules_to_blueprint(api)

