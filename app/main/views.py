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
        logger.info('redirecting for current_group {}'.format(current_group))
        # divert to user group homepage for authenticated users
        return( redirect( url_for('main.home', gpid=current_group )))
    else:
        current_group = 1

    logger.info('still in index with current_group {}'.format(current_group))
    topic = Info.query.filter_by(group=current_group).order_by('seq').all()
    return render_template('index.html', topic_dict=topic)

# List all topics for specified group
@main.route('/home/<int:gpid>')
@login_required
def home(gpid):
    # set user.current_group
    current_user.current_group = gpid
    db.session.add(current_user)
    db.session.commit()
    
    topics = Topic.query.filter_by(group=gpid).order_by(Topic.discussion_datetime).all()
    
    ttlist = []
    if topics:
        for topic in topics:
            #tt = topic.dump()
            #print('tt: ',tt)
            #assert( isinstance(tt,dict))
            ttlist.append( topic.dump() )
    # If this group requires registration filter out
    #print('opgroup: ',opgroup.dump())
    #logger.info('gp.dump()'.format( opgroup))
    return render_template('home.html', gp=gpid, tt=ttlist )

################################## info ######################################################################
'''
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