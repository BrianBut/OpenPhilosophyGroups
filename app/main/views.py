from datetime import datetime
from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
#from .forms import EditTopicForm, DeleteTopicForm, EditProfileForm, NewCommentForm, EditCommentForm, NewTopicForm, EditTopicForm, EmailForm
from .forms import InfoForm
from .. import db
from ..models import Topic, User, Role, Comment, MailList, Info, Group
from ..decorators import member_required, admin_required, moderator_required
from . import main
from ..loggingPA import logger

@main.route('/')
def index():
    if current_user.is_authenticated:
        current_group = User.query.get_or_404(current_user.id).current_group
        logger.info('current_group {}'.format(current_group))
        # divert to user group homepage
    else:
        current_group = 1

    
    topic = Info.query.filter_by(group=current_group).order_by('seq').all()
    return render_template('index.html', topic_dict=topic)

    #u = User.query.get_or_404(id).first()
    #available = Group.get.filter_by(current_group)

    #g = Group.query.get.filter


################################## info ######################################################################
# 6 May 2024
@main.route('/new_info', methods=['GET','POST'])
@login_required
@moderator_required
def new_info():
    form=InfoForm()
    if request.method == 'POST' and form.validate():
        info=Info( title=form.title.data, content=form.content.data, group=current_user.current_group, author_id=current_user.id )
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newinfo.html',form=form)

@main.route('/edit_info/<int:id>', methods=['GET','POST'])
@login_required
@moderator_required
def edit_info(id):
    info = Info.query.get_or_404(id)
    logger.info('info {}'.format( info.dump() ))
    form=InfoForm(info=info)
    if request.method == 'POST' and form.validate():
        info.title = form.title.data
        info.content = form.content.data
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('.index'))
    form.title.data=info.title
    form.content.data=info.content
    return render_template('newinfo.html',form=form)
'''
@main.route('/edittopic/<int:id>', methods=['GET','POST'])
@login_required
@member_required
def edittopic(id):
    topic=Topic.query.get_or_404(id)
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
        return redirect(url_for('.topic',topic_id=id))
    form.title.data=topic.title
    form.summary.data=topic.summary
    form.content.data=topic.content
    form.published.data = topic.published
    return render_template('edittopic.html',form=form)
'''

################################ Moderator or Administrator #######################################################
@main.route('/setmeetingtime/<int:topic_id>', methods=['GET','POST'])
@login_required
@moderator_required
def setmeetingtime(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    form = SetMeetingTimeForm( topic_id=topic_id )
    if request.method == 'POST' and form.validate():
        topic.discussion_datetime=datetime.combine(form.discussion_date.data, form.discussion_time.data)
        db.session.add(topic)
        db.session.commit()
        return redirect( url_for('.topic', topic_id=topic_id))
    form.discussion_datetime = topic.discussion_datetime
    return render_template('setmeetingtime.html', form=form)


@main.route('/mailaddresses', methods=['GET','POST'])
@login_required
@moderator_required
def mailaddresses():
    addresses = MailList.query.order_by('email').all()
    return render_template("mailaddresses.html", addresses=addresses)
