from functools import wraps
from graphql import GraphQLError

def role_required(required_roles):
    """
    Decorator to restrict access to queries and mutations based on user roles.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise GraphQLError("Authentication required")

            user_roles = user.groups.values_list('name', flat=True)
            
            if not any(role in required_roles for role in user_roles):
                raise GraphQLError("You do not have the required permissions to access this resource")
            
            return func(root, info, *args, **kwargs)
        return wrapper
    return decorator
