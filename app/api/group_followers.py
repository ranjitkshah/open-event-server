from flask_jwt_extended import current_user, jwt_required
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

from app.api.helpers.errors import ConflictError
from app.api.helpers.utilities import require_relationship
from app.api.schema.group_followers import GroupFollowerSchema
from app.models import db
from app.models.group import Group
from app.models.group_follower import GroupFollower


class GroupFollowerListPost(ResourceList):
    """
    Create Group Follower
    """

    @classmethod
    def before_post(cls, args, kwargs, data):
        """
        before post method to check for required relationship and proper permission
        :param args:
        :param kwargs:
        :param data:
        :return:
        """
        require_relationship(['group'], data)

        print(current_user.id)
        data['user'] = current_user.id
        group_followed_user = GroupFollower.query.filter_by(user=current_user).first()
        if group_followed_user:
            raise ConflictError(
                {'pointer': '/data/relationships/session'}, "Group already followed"
            )

    view_kwargs = True
    decorators = (jwt_required,)
    schema = GroupFollowerSchema
    methods = [
        'POST',
    ]
    data_layer = {
        'session': db.session,
        'model': GroupFollower,
        'methods': {'before_post': before_post},
    }


class UserGroupFollowedList(ResourceList):
    """
    List User Followed groups
    """

    def query(self, view_kwargs):
        query_ = GroupFollower.query
        if view_kwargs.get('user_id'):
            user = safe_query_kwargs(User, view_kwargs, 'user_id')
            if user != current_user and not (
                (is_logged_in() and has_access('is_admin')) or user.is_profile_public
            ):
                raise ForbiddenError({'pointer': 'user_id'})
            query_ = query_.filter_by(user_id=user.id)

        elif view_kwargs.get('group_id'):
            group = safe_query_kwargs(Group, view_kwargs, 'group_id')
            query_ = query_.filter_by(group_id=group.id)

        # elif view_kwargs.get('event_id'):
        #     event = safe_query_kwargs(Event, view_kwargs, 'event_id')
        #     query_ = query_.join(UserFavouriteSession.session).filter_by(
        #         event_id=event.id
        #     )

        elif not has_access('is_admin'):
            raise ForbiddenError({'pointer': 'user_id'}, 'Admin Access Required')

        return query_

    methods = ['GET']
    schema = GroupFollowerSchema
    data_layer = {
        'session': db.session,
        'model': GroupFollower,
        'methods': {'query': query},
    }


class UserGroupFollowedDetail(ResourceDetail):
    """
    User followed group detail by id
    """

    @staticmethod
    def check_perm(fav):
        if not has_access(
            'is_coorganizer_or_user_itself',
            # event_id=fav.session.event_id,
            user_id=fav.user_id,
        ):
            raise ForbiddenError(
                {'pointer': 'user_id'}, "User or Co-Organizer level access required"
            )

    def after_get_object(self, fav, view_kwargs):
        UserGroupFollowedDetail.check_perm(fav)

    def before_delete_object(self, fav, view_kwargs):
        UserGroupFollowedDetail.check_perm(fav)

    methods = ['GET', 'DELETE']
    decorators = (jwt_required,)
    schema = GroupFollowerSchema
    data_layer = {
        'session': db.session,
        'model': GroupFollower,
        'methods': {
            'after_get_object': after_get_object,
            'before_delete_object': before_delete_object,
        },
    }


class UserGroupFollowedRelationship(ResourceRelationship):
    """
    User Followed Group Relationship
    """

    schema = GroupFollowerSchema
    decorators = (jwt_required,)
    methods = ['GET']
    data_layer = {'session': db.session, 'model': GroupFollower}
