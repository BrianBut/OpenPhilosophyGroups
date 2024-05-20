#from datetime import datetime
#from pathlib import Path
from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .forms import NewGroupForm
from .. import db
from ..models import User, Group, Category, Topic
from ..decorators import member_required, admin_required, moderator_required
from . import groups
from ..loggingPA import logger

'''
@groups.route('categories')
@login_required
def opgroups():
    categories = Category.query.order_by('id').all()
    print('categories: ',categories)
    return render_template('groups/groups.html', categories=categories )
'''

# List all groups with options to join
@groups.route('groups')
@login_required
def opgroups():
    categories = Category.query.order_by('id').all()
    print('categories: ',categories)
    groups = Group.query.group_by(Group.category_id).all()
    return render_template('groups/groups.html', groups=groups, categories=categories )

# List all topics for specified group
@groups.route('opgroup/<int:gpid>')
@login_required
def opgroup(gpid):
    # set user.current_group
    current_user.current_group = gpid
    db.session.add(current_user)
    db.session.commit()

    gp = Group.query.get_or_404(gpid)
    logger.info("/opgroup got group {}".format(gp.groupname))
    
    tl = { 'proposed_topics':[], 'future_topics':[], 'past_topics':[], 'online_topics':[] }
    topics = Topic.query.filter_by(group=gpid).order_by(Topic.discussion_datetime).all()
    for topic in topics:
        tt = topic.dump()
        assert( isinstance(tt,dict))
        assert(tt['venue'] in ['proposed','online','planned','past'])
        tt['url'] = url_for('topics.topic', tid=topic.id )
        if tt['venue'] == 'proposed':
            tl['proposed_topics'].append(tt)
        elif tt['venue'] == 'online':
            tl['online_topics'].append(tt)
        elif tt['venue'] == 'planned':
            tl['future_topics'].append(tt)
        elif tt['venue'] == 'past':
            tl['past_topics'].append(tt)
        else: 
            #print('venue is:', tt['venue'])
            raise Exception("get_topics failed to find venue") 
        #print(topic.discussion_datetime.strftime('%s'), tt['venue'] )

    # If this group requires registration filter out
    #print('opgroup: ',opgroup.dump())
    #logger.info('gp.dump()'.format( opgroup))
    return render_template('home.html', gp=gp, tt_list=tl )

# This may not be better reached from the group page! 
@groups.route( 'delete<int:grid>', methods=['POST','GET'])
@login_required
def delete(gpid):
    form = DeleteGroupForm()
    if request.method == 'POST' and form.validate():
        return redirect(url_for('group.group'))
    return render_template('groups/groups.html', form=form)


@groups.route( 'new_group', methods=['POST', 'GET'])
@login_required
def new_group():
    categories = Category.query.filter( Category.description != None).all()
    nncategories = [ c for c in categories if c.description ]
    #print( 'nncategories', nncategories )
    choices = []
    for c in nncategories:
        choices.append( [ str(c.id),c.description] )
    #print('choices: ', choices )
    form = NewGroupForm()
    form.category.choices = choices
    if request.method == 'POST' and form.validate():
        if Group.query.filter_by(groupname=form.groupname.data).first():
            flash(category='info', message='A group with the name {} already exists. You cannot form a new group with this name'.format(groupname))
            logger.info("Group Exists so redirecting to new_group")
            return redirect(url_for('groups.new_group'))
        print('groupname: ', form.groupname.data)
        print('founder: ', current_user.id)
        print('category_id: ', form.category.data)
        gp = Group(groupname=form.groupname.data, founder=current_user, category_id=form.category.data )
        print( "group: ",gp )
        db.session.add(gp)
        db.session.commit() 
        return redirect(url_for('main.home', gpid=gp.id))
    return render_template('groups/new_group.html', form=form)
'''
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
    form = SelectActiveGroupForm( default= user.current_group) submit = SubmitField('Submit')

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