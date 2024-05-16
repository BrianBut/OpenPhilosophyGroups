from flask import Blueprint

topics = Blueprint('topics', __name__)

from . import views
#from ..models import Group, Category

#@main.app_context_processor
#def inject_permissions():
#    return dict(Permission=Permission)