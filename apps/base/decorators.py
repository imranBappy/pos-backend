from graphql.execution.base import ResolveInfo
from graphql_jwt.decorators import login_required

def role_required(allowed_roles):
    """
    Restricts access to users with specified roles.
    :param allowed_roles: List of roles (e.g., ["ADMIN", "CHEF"])
    """
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(root, info: ResolveInfo, *args, **kwargs):
            user = info.context.user
            if user.role not in allowed_roles:
                raise Exception("Permission Denied: You do not have the required role.")
            return func(root, info, *args, **kwargs)
        return wrapper
    return decorator