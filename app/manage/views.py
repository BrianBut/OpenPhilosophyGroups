#from datetime import datetime
#from pathlib import Path
from flask import render_template, redirect, request, url_for
from flask_login import current_user
from flask_login import login_required
from .forms import RescheduleTopicForm, ConfirmDeleteForm, EditUserForm, NewGroupForm, EditGroupForm, TodoForm, ROLE_CHOICES
from .. import db
from ..models import Group, Topic, User, Role, Todos, MailList
from ..decorators import admin_required, moderator_required
from datetime import datetime, timezone
from . import manage

from ..loggingPA import logger

# List all users
@manage.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.email).all()
    for user in users:
        user.role_name = ROLE_CHOICES[ user.role_id][1]
    return render_template("manage/users.html", users=users)
'''
@manage.route('/manage/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user( id ):
    user = User.query.get_or_404(id)
    form = ConfirmDeleteForm(user=user)
    if request.method == 'POST' and form.validate():
        if form.confirmed.data == True:
            db.session.delete( user )
            db.session.commit()
        return redirect(url_for('manage.users'))
    return render_template("manage/confirm_delete_user.html",form=form, user=user )

@manage.route('/edit_user/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_user(id):
    user=User.query.get_or_404(id)
    choices=Role.query.all()
    #print("choices: ",choices)
    form = EditUserForm(user=user)
    form.choices=choices
    if request.method == 'POST' and form.validate():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data 
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('manage.users'))
    form.email.data=user.email
    form.confirmed.data=user.confirmed
    return render_template('manage/edit_user.html', form=form )


@manage.route('/reschedule/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def reschedule( id ):
    topic = Topic.query.get_or_404(id)
    print('topic: {}, datetime: {}, published: {}'.format(topic.id, topic.discussion_datetime, topic.published ))
    form = RescheduleTopicForm( topic=topic )
    if request.method == 'POST' and form.validate():
        topic.published = form.published.data
        topic.discussion_datetime = form.discussion_datetime
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('manage.topics', topics=topic ))
    form.discussion_datetime.data = topic.discussion_datetime
    return render_template("/manage/reschedule.html", form=form )

@manage.route('/delete_topic', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_topic():
    return render_template("index.html")
'''
####################### todo_topics #######################

@manage.route("/newtodo",methods=['GET','POST'])
@login_required
@admin_required
def new_todo():
    form = TodoForm()
    if request.method == 'POST' and form.validate():
        todo = Todos(content=form.content.data,author_id=current_user.id, creation_datetime=datetime.now)
        todo.creation_datetime=datetime.now(tz=timezone.utc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('manage.todos'))
    form.group.data = current_user.current_group
    return render_template("manage/newtodo.html", form=form )


@manage.route('todos')
@login_required
@admin_required
def todos():
    notdone = Todos.notdone()
    done = Todos.done()
    return render_template("manage/todos.html", notdone=notdone, done=done )


@manage.route('mark_done/<tdid>', methods=['POST','GET'])
@login_required
@admin_required
def mark_done( tdid ):
    todo = Todos.query.get( tdid )
    todo.completion_datetime = datetime.now(tz=timezone.utc)
    db.session.add( todo )
    db.session.commit()
    return redirect(url_for('manage.todos'))

@manage.route('mark_undone/<tdid>', methods=['POST','GET'])
@login_required
@admin_required
def mark_undone( tdid ):
    todo = Todos.query.get( tdid )
    todo.completion_datetime = datetime.max
    logger.info('todo marked_unddone: {}'.format( todo.dump()))
    db.session.add( todo )
    db.session.commit()
    return redirect(url_for('manage.todos'))

###################### groups #############################
# This is for admin use
#@manage.route('/groups')
#@login_required
#@admin_required
#def groups():
#    groups = Group.query.order_by(Group.groupname).all()
#    return render_template("manage/groups.html", groups=groups)
'''
@manage.route("/groupmembership/<int:gpid>")
@login_required
@admin_required
def groupmembership(gpid):
    group = Group.query.filter_by(id=gpid).first()
    memberlist = []
    users = User.query.all()
    for user in users:
        if gpid in user.mygrouplist():
            memberlist.append(user)
        current_user.addgroup()
    return render_template("manage/groupmembership.html", group=group, memberlist=memberlist)


@manage.route("/newgroup",methods=['GET','POST'])
@login_required
@admin_required
def new_group():
    form = NewGroupForm()
    if request.method == 'POST' and form.validate():
        group=Group(groupname=form.groupname.data)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('manage.groups'))
    return render_template("manage/newgroup.html", form=form )

@manage.route("/editgroup/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def edit_group(id):
    group = Group.query.get_or_404(id)
    form = EditGroupForm(group=group)
    if request.method == 'POST' and form.validate():
        group.groupname=form.groupname.data
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('manage.groups'))
    return render_template("manage/newgroup.html", form=form )

''' 
@manage.route('/setmeetingtime/<int:topic_id>', methods=['GET','POST'])
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

######################################## Sundry #######################################
@manage.route('/mailaddresses', methods=['GET','POST'])
@login_required
@moderator_required
def mailaddresses():
    addresses = MailList.query.order_by('email').all()
    return render_template("/manage/mailaddresses.html", addresses=addresses)

