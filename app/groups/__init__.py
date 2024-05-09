from flask import Blueprint

groups = Blueprint('groups', __name__)

from . import views
#from ..models import Group, Category

#@main.app_context_processor
#def inject_permissions():
#    return dict(Permission=Permission)