from datetime import datetime
from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
#from .forms import EditTopicForm, DeleteTopicForm, EditProfileForm, NewCommentForm, EditCommentForm, NewTopicForm, EditTopicForm, EmailForm
from .forms import InfoForm
from .. import db
from ..models import Topic, User, Role, Comment, MailList, Info, Group, GroupDoes
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

    tl = { 'proposed_topics':[], 'future_topics':[], 'past_topics':[], 'online_topics':[] }

    group = Group.query.get_or_404(gpid)
    for topic in topics:
        tt = topic.dump()
        assert( isinstance(tt,dict))
        assert(tt['venue'] in ['proposed','online','planned','past'])
        tt['url'] = url_for('topics.topic', tid=topic.id )
        if group.has_meetings():
            logger.info('group {} has meetings'.format(group.id))
            if tt['venue'] == 'proposed':
                tl['proposed_topics'].append(tt)
            elif tt['venue'] == 'online':
                tl['online_topics'].append(tt)
            elif tt['venue'] == 'planned':
                tl['future_topics'].append(tt)
            elif tt['venue'] == 'past':
                tl['past_topics'].append(tt)
            else: 
                raise Exception("get_topics failed to find venue") 
        else:
            tl['online_topics'].append(tt)
    
    # If this group requires registration filter out
    #print('opgroup: ',opgroup.dump())
    #logger.info('gp.dump()'.format( opgroup))
    return render_template('home.html', gp=gpid, tt_list=tl, meets=group.has_meetings() )

################################## info ######################################################################

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
