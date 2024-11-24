import graphene
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.db import transaction
from graphql_jwt.decorators import login_required
from .models import User as CustomUser, UserRole
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.shortcuts import get_token

class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @transaction.atomic
    def mutate(self, info, name, email, password):
        # if role not in UserRole.values:
        #     return RegisterUser(success=False, message="Invalid role provided.")
        
        if CustomUser.objects.filter(email=email).exists():
            return RegisterUser(success=False, message="Email is already registered.")
        
        user = CustomUser.objects.create_user(
            name=name, email=email, password=password
        )
        user.is_verified = False  # Email verification can be implemented separately
        user.save()

        return RegisterUser(success=True, message="Registration successful!")



class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, email, password):
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                return LoginUser(token=None, success=False, message="Invalid email or password.")
            if not user.is_active:
                return LoginUser(token=None, success=False, message="Account is inactive.")
            token = get_token(user)
            return LoginUser(token=token, success=True, message="Login successful.")
        except User.DoesNotExist:
            return LoginUser(token=None, success=False, message="Invalid email or password.")


# class ResetPassword(graphene.Mutation):
#     class Arguments:
#         email = graphene.String(required=True)

#     success = graphene.Boolean()
#     message = graphene.String()

#     def mutate(self, info, email):
#         try:
#             user = CustomUser.objects.get(email=email)
#         except ObjectDoesNotExist:
#             return ResetPassword(success=False, message="No user found with this email.")

#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         reset_link = f"http://example.com/reset-password/{uid}/{token}/"

#         # Send the reset password email
#         send_mail(
#             subject="Password Reset",
#             message=f"Use this link to reset your password: {reset_link}",
#             from_email="noreply@example.com",
#             recipient_list=[email],
#         )

#         return ResetPassword(success=True, message="Password reset email sent.")


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    # reset_password = ResetPassword.Field()
