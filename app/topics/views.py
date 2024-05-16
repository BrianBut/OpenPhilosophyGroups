from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .forms import NewTopicForm, EditTopicForm
from .. import db
from ..models import User, Group, Topic
from ..decorators import member_required, admin_required, moderator_required
from . import topics
from ..loggingPA import logger

#Presents a form to create a new topic.
#Note title is not unique as there are multiple groups
@topics.route( 'new_topic', methods=['POST', 'GET'])
@login_required
def new_topic():
    form = NewTopicForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        if Topic.query.filter_by(group=current_user.current_group).first():
            flash(category='info', message='A topic with this title ({}) already exists. You cannot form a new topic with this title'.format(title))
            logger.info("Title Exists so redirecting to new_group")
            return redirect(url_for('topics.new_topic'))
        topic = Topic(group=current_user.current_group, title=title, summary=form.summary.data, author_id=current_user.id )
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topics.topic', tid=topic.id ))
    return render_template('topics/new_topic.html', form=form)


# Presents a form to edit a topic, both summary and content.
# Limitations on summary
@topics.route('edit_topic', methods=['POST', 'GET'])
@login_required
def edit_topic(tid):
    form = EditTopicForm()
    return render_template('topics/edit_topic.html', form=form)

    
# Presents summary, content and comments for a topic.
@topics.route('topic/<int:tid>')
@login_required
def topic(tid):
    return render_template('topics/topic.html')


#lists all topics within the group, sorting by 'pending','proposed','online_only'
@topics.route('topics')
@login_required
def topics():
    sorted_topics = []
    return render_template('topics/topics.html', topics=sorted_topics)