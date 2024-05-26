from datetime import datetime, timezone
from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .forms import EditTopicForm, DeleteTopicForm, NewCommentForm, EditCommentForm, NewTopicForm, EditTopicForm, InfoForm, NewInfoForm
from .. import db
from ..models import Topic, User, Role, Comment, MailList, Info, Group, InfoCategoryChoices
from ..decorators import member_required, admin_required, moderator_required
from . import main
from ..loggingPA import logger

@main.route('/')
def index():
    if current_user.is_authenticated:
        current_group = User.query.get_or_404(current_user.id).current_group
    #    logger.info('redirecting for current_group {}'.format(current_group))
        # divert to user group homepage for authenticated users
    #    return( redirect( url_for('main.home', gpid=current_group )))
    else:
        current_group = 1 

    info = Info.query.filter_by(group_id=current_group).order_by('priority').first()
    return render_template('index.html', info=info)


# List all topics for specified group
@main.route('/home/<int:gpid>')
@login_required
def home(gpid):
    group = Group.query.get(gpid)
    current_user.current_group = group.id
    db.session.add(current_user)
    db.session.commit()

    # if the group has 'preamble' info, display them
    infos = Info.query.filter_by(info_category=1).filter_by(group_id=group.id).order_by('priority').all()
    for info in infos:
        print('info: ',info)

    # If the group has meetings order by discussion_datetime, Info prioriy undecided
    if 'meet' in group.category.description:
        topiclist = [ topic.dump() for topic in Topic.query.filter_by(group=gpid).order_by(Topic.creation_datetime).order_by(Topic.discussion_datetime).all() ]
        return render_template('home.html', gp=gpid, topiclist=topiclist )
    
    elif 'nline' in group.category.description:
        topiclist = [ topic.dump() for topic in Topic.query.filter_by(group=gpid).order_by(Topic.creation_datetime).all() ]
        return render_template('home.html', gp=gpid, topiclist=topiclist )

    elif 'Info' in group.category.description:
        topiclist = [ topic.dump() for topic in Topic.query.filter_by(group=gpid).order_by(Topic.creation_datetime).order_by(Topic.discussion_datetime).all() ]
        return  render_template('home.html', gp=gpid, topiclist=topiclist )
    
    elif 'Necessary' in group.category.description:
        topiclist = [ topic.dump() for topic in Topic.query.filter_by(group=gpid).order_by(Topic.creation_datetime).all() ]

    logger.info('no topiclist found for group {} with description {}'.format(group, group.category.description))

    return render_template('home.html', gp=gpid, infos=infos, topiclist=topiclist )
    

@main.route('/new_topic', methods=['GET', 'POST'])  
@login_required  
def new_topic():
    form = NewTopicForm()
    if request.method == 'POST' and form.validate():
        # form validator needs to check title is unique
        #if Topic.query.filter_by(group=current_user.current_group).first():
        #    flash(category='info', message='A topic with this title ({}) already exists. You cannot form a new topic with this title'.format(title))
        #    logger.info("Title Exists so redirecting to new_group")
        #    return redirect(url_for('topics.new_topic'))
        topic = Topic(group=current_user.current_group, title=form.title.data, summary=form.summary.data, author=current_user )
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('main.topic', tid=topic.id ))
    return render_template('/new_topic.html', form=form)


# Presents a form to edit a topic, both summary and content.
@main.route('/edit_topic/<int:id>', methods=['GET','POST'])
@login_required
def edit_topic(id):
    topic=Topic.query.get_or_404(id)
    group = Group.query.get_or_404(current_user.current_group)
    form=EditTopicForm(topic=topic)
    if request.method == 'POST' and form.validate():
        topic.title = form.title.data
        topic.summary=form.summary.data
        topic.content=form.content.data
        topic.published=form.published.data
        topic.last_edited_datetime=datetime.now(tz=timezone.utc)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.topic',tid=id))
    form.title.data=topic.title
    form.summary.data=topic.summary
    form.content.data=topic.content
    form.published.data = topic.published
    return render_template('/edit_topic.html',form=form)

    
# Presents summary, content and comments for a topic.
@main.route('/topic/<int:tid>')
@login_required
def topic(tid):
    t = Topic.query.get_or_404( tid )
    comments = Comment.query.filter_by(topic_id=tid).order_by('creation_datetime').all()
    cds = []
    for c in comments:
        cds.append(c.dump())
    #print( "cds: {}".format( cds ))
    return render_template('/topic.html', topic=t, commentsd=cds )


# An administrator can always delete a topic
# A creator can delete a topic for up to 48 hours from its creation
# A topic with no content and no comments will automatically be deleted after 2 days
@main.route('delete_topic/<int:tid>', methods=['POST', 'GET'])
@login_required
def delete_topic( tid ):
    if not current_user.is_administrator:
        flash( category='Danger', message='Check for conditions not yet implemented')
        return redirect( url_for('main.topic',tid=tid))
    
    topic=Topic.query.get_or_404(tid)
    form = DeleteTopicForm(topic=topic)
    if request.method == 'POST' and form.validate():
        db.session.delete(topic) 
        db.session.commit()
        flash( category='Info', message='topic and all its comments deleted')
        return redirect(url_for('main.home'))
    #print('Summary: {}'.format(topic.summary))
    form.summary.data=topic.summary
    form.title.data=topic.title
    return render_template('delete_topic.html',form=form)


@main.route( 'new_comment/<int:topic_id>', methods=['POST', 'GET'])
@login_required
def new_comment(topic_id):
    form = NewCommentForm()
    if request.method == 'POST' and form.validate():
        topic_id = topic_id
        comment = Comment(content=form.content.data, topic_id=topic_id, author_id=current_user.id, edit_datetime=datetime.now(tz=timezone.utc))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.topic', tid=topic_id ))
    return render_template('/new_comment.html', form=form)


@main.route( 'edit_comment/<int:comment_id>', methods=['POST', 'GET'])
@login_required
def edit_comment(comment_id):
    form = EditCommentForm()
    comment = Comment.query.get_or_404(comment_id)
    if request.method == 'POST' and form.validate():
        topic_id = comment.topic.id
        new_comment = Comment(content=form.content.data, topic_id=topic_id, author_id=current_user.id, edit_datetime=datetime.now(tz=timezone.utc))
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.topic', tid=topic_id ))
    
    form.topic_id.data = comment.topic_id
    form.author_id.data = comment.author_id
    form.content.data = comment.content
    title = comment.topic.title
    return render_template('/edit_comment.html', form=form, title=title)

################################## info ######################################################################

@main.route('/new_info', methods=['GET','POST'])
@login_required
@moderator_required
def new_info():
    form=NewInfoForm()
    form.info_category.choices = InfoCategoryChoices
    if request.method == 'POST' and form.validate():
        info=Info( content=form.content.data, info_category=int(form.info_category.data), group_id=current_user.current_group, owner_id=current_user.id )
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newinfo.html',form=form)

@main.route('/edit_info/<int:id>', methods=['GET','POST'])
@login_required
@moderator_required
def edit_info(id):
    info = Info.query.get_or_404(id)
    # if there is no info create a new form
    if info == None:
        flash(category='danger', message='You attempted to edit nonexistent info: Redirecting to "new_info.html"')
        return redirect(url_for('.new_info'))
    form=InfoForm(info=info)
    if request.method == 'POST' and form.validate():
        #info.title = form.title.data
        info.content = form.content.data
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('.index'))
    form.content.data=info.content
    return render_template('edit_info.html',form=form)

