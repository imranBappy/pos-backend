from functools import wraps
from graphene import ResolveInfo
from graphql import GraphQLError


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator


def user_passes_test(
    test_func,
    exc_factory=lambda: GraphQLError(
        message="Unauthorized user!",
        extensions={
            "error": "You are not authorized user.",
            "code": "unauthorized",
        },
    ),
):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exc_factory()
        return wrapper
    return decorator


def custom_authentication_logic(user):
    try:
        return user.is_authenticated
    except Exception as e:
        raise GraphQLError(
            message="Unauthorized user!",
            extensions={
                "error": "You are not authorized user.",
                "code": "unauthorized",
            },
        )


def custom_permission_logic(user):
    try:
        custom_authentication_logic(user)
        return user.is_admin
    except Exception as e:
        raise GraphQLError(
            message="User is not permitted.",
            extensions={
                "error": "You are not authorized to perform operations.",
                "code": "invalid_permission",
            },
        )


login_required = user_passes_test(
    custom_authentication_logic,
    exc_factory=lambda: GraphQLError("Custom Authentication Required"),
) 
admin_required = user_passes_test(
    custom_permission_logic,
    exc_factory=lambda: GraphQLError("Admin Permission Required"),
)
