#from datetime import datetime
#from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .forms import SelectActiveGroupForm, NewGroupForm, DeleteGroupForm
from .. import db
from ..models import User, Group, GroupDoes
from ..decorators import member_required, admin_required, moderator_required
from . import groups
from ..loggingPA import logger

@groups.route('groups')
@login_required
def opgroups():
    user=User.query.filter_by(id=current_user.id).first()
    groups = Group.query.order_by('groupname').all()
    categories = [ [], [], [], [], [], [] ]

    for group in groups:
        if group.is_todo():
            group.cat = 'Todo'
            categories[0].append(group)
        elif group.requires_registration():
            group.cat = 'Requires Registration and may be restricted'
            categories[1].append(group)
        elif group.has_meetings():
            group.cat = 'This Group has Meetings'
            categories[2].append(group)
        elif group.is_necessary():
            group.cat = 'Necessary'
            categories[3].append(group)
        elif group.is_info():
            group.cat = 'Info'
            categories[4].append(group)
        else:
            group.cat = 'Information Only'
            categories[5].append(group)

    return render_template('groups/groups.html', categories=categories )


@groups.route( 'delete<int:grid>', methods=['POST','GET'])
@login_required
def delete(gpid):
    form = DeleteGroupForm()
    if request.method == 'POST' and form.validate():
        return redirect(url_for('group.group'))
    return render_template('groups/groups.html', form=form)

'''
@groups.route( 'new_group', methods=['POST', 'GET'])
@login_required
def new_group():
    form = NewGroupForm()
    if request.method == 'POST' and form.validate():
        groupname=form.groupname.data
        if Group.query.filter_by(groupname=groupname).first():
            flash(category='info', message='A group with the name {} already exists. You cannot form a new group with this name'.format(groupname))
            logger.info("Group Exists so redirecting to new_group")
            return redirect(url_for('groups.new_group'))
        gp = Group(groupname=form.groupname.data, founder=current_user.id, category=0 )
        if form.has_meetings:
            gp.set( GroupDoes.MEETING )
        if form.is_online_only:
            gp.set( GroupDoes.ONLINE )
        if form.requires_registration:
            gp.set( GroupDoes.REGISTRATION )
        db.session.add(gp)
        db.session.commit() 
        return redirect(url_for('main.home', gpid=gp.id))
    return render_template('groups/new_group.html', form=form)

# Select a group from those in user.groups
@groups.route('select_active', methods=['POST', 'GET'])
@login_required
def select_active():
    user=User.query.get( current_user.id)
    form = SelectActiveGroupForm()
    form.data.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
    logger.info('choices: {}'.format( form.data.choices))
    #logger.info('from form select_active choices: {}'.format(form.data['choices']))
    return render_template('groups/select_active.html', form=form)


@groups.route('select_active_group', methods=['POST','GET'])
@login_required
def select_active():
    user = User.query.get(current_user.id)
    logger.info('user.current_group: {}'.format(user.current_group))
    allgroups = Group.query.all()
    choices = []
    for group in allgroups:
        choices.append( (group.id, group.groupname) )
    form = SelectActiveGroupForm( default= user.current_group) 
    form.selected_group.choices = choices
    #form.selected_group.default = str(user.current_group)
    print('choices: ', form.selected_group.choices)
    if request.method == 'POST' and form.validate():
        logger.info('form.selected_group.data: {}'.format(form.selected_group.data))
        user.current_group=form.selected_group.dataapp/templates/manage/groups.html
        db.session.add( user )
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('/groups/groups.html', form=form)




@groups.route('membership', methods=['GET'])
@login_required
def membership():
    user = User.query.get(current_user.id)
    # List of all groups user is a member of
    grls = user.mygrouplist()
    print('grs: ',grls)
    mygroups = []
    for grp in grls:
        g = Group.query.filter_by(id=grp).first()
        mygroups.append(g)
    return render_template('/groups/membership.html', mygroups=mygroups )

# Open groups are other groups that a user may elect to join
@groups.route('opengroups', methods=['GET'])
@login_required
def opengroups():
    opengrps = []
    can_apply = []
    groups = Group.query.all()
    for group in groups:
        if group.id in current_user.mygrouplist():
            continue
        #if group.members_only and group.is_on_register(current_user.id):
        #    can_apply.append(group.id)
        #    continue
        opengrps.append(group)
    return render_template('/groups/opengroups.html', opengroups=opengrps, can_apply=can_apply )

@groups.route('join/<int:user_id>/<int:group_id>', methods=['GET','POST'])
@login_required
def join( user_id, group_id):
    user = User.query.get(user_id)
    group = Group.query.get(group_id)
    #if group.registration_required:
    #    flash(category='Info', message='We need to contact the group moderator')
    #    pass
    user.addgroup(group.id)
    user.current_group=group.id
    db.session.commit()
    return redirect(url_for('main.index'))

'''