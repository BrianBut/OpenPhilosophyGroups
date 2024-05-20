from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime, timezone
from pathlib import Path
from .forms import NewTopicForm, EditTopicForm, NewCommentForm
from .. import db
from ..models import Group, Topic, Comment
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
        #if Topic.query.filter_by(group=current_user.current_group).first():
        #    flash(category='info', message='A topic with this title ({}) already exists. You cannot form a new topic with this title'.format(title))
        #    logger.info("Title Exists so redirecting to new_group")
        #    return redirect(url_for('topics.new_topic'))
        topic = Topic(group=current_user.current_group, title=form.title.data, summary=form.summary.data, author=current_user )
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topics.topic', tid=topic.id ))
    return render_template('topics/new_topic.html', form=form)


# Presents a form to edit a topic, both summary and content.
@topics.route('/edittopic/<int:id>', methods=['GET','POST'])
@login_required
def edittopic(id):
    topic=Topic.query.get_or_404(id)
    group = Group.query.get_or_404(current_user.current_group)
    form=EditTopicForm(topic=topic)
    if request.method == 'POST' and form.validate():
        topic.title = form.title.data
        topic.summary=form.summary.data
        topic.content=form.content.data
        topic.published=form.published.data
        #print('setting content data to {}'.format(topic.content))
        #print('setting published data to {}'.format(topic.published)) 
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.topic',tid=id))
    form.title.data=topic.title
    form.summary.data=topic.summary
    form.content.data=topic.content
    form.published.data = topic.published
    return render_template('topics/edit_topic.html',form=form)


    
# Presents summary, content and comments for a topic.
@topics.route('topic/<int:tid>')
@login_required
def topic(tid):
    t = Topic.query.get_or_404( tid )
    comments = Comment.query.filter_by(topic_id=tid).order_by('creation_datetime').all()
    cds = []
    for c in comments:
        cds.append(c.dump())
    #print( "cds: {}".format( cds ))
    return render_template('topics/topic.html', topic=t, commentsd=cds )


@topics.route( 'new_comment/<int:topic_id>', methods=['POST', 'GET'])
@login_required
def new_comment(topic_id):
    form = NewCommentForm()
    if request.method == 'POST' and form.validate():
        topic = Topic.query.get_or_404(topic.id)
        comment = Comment(content=form.content.data, topic=topic, author=current_user, edit_datetime=datetime.now(tz=timezone.utc))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('topics.topic', tid=topic.id ))
    return render_template('topics/new_comment.html', form=form)

