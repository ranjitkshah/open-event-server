from flask_jwt_extended import current_user, jwt_required
from flask_rest_jsonapi import ResourceList

from app.api.helpers.errors import ConflictError
from app.api.helpers.utilities import require_relationship
from app.api.schema.group_followers import GroupFollowerSchema
from app.models import db
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
