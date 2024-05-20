# models.py
from app import db
from .mymodels.groupmodel import Group, Category
from .mymodels.maillistmodel import MailList
from .mymodels.usermodel import Group, Permission, Role, User, AnonymousUser
from .mymodels.topicmodel import Comment, Topic
from .mymodels.infomodel import Info
from .mymodels.todomodel import Todos


