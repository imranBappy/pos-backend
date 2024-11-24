import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token, create_refresh_token
from django.contrib.auth.models import Group
from .permissions import role_required

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "name", "photo", "is_verified", "gender", "date_of_birth")

class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, email, password, name):
        user = User.objects.create_user(email=email, password=password, name=name)
        token = get_token(user)
        return RegisterUser(user=user, token=token)

class AssignRole(graphene.Mutation):
    user = graphene.Field(UserType)
    group_name = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        group_name = graphene.String(required=True)

    def mutate(self, info, email, group_name):
        try:
            user = User.objects.get(email=email)
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            user.save()
            return AssignRole(user=user, group_name=group_name)
        except User.DoesNotExist:
            raise Exception("User does not exist")

class LoginMutation(graphene.Mutation):
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        from django.contrib.auth import authenticate
        user = authenticate(email=email, password=password)
        if not user:
            raise Exception("Invalid credentials")

        token = get_token(user)
        return LoginMutation(token=token)

class PrivateData(graphene.ObjectType):
    secret_message = graphene.String()

    def resolve_secret_message(self, info):
        return "This is a private message only accessible to Admins"
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    private_data = graphene.Field(PrivateData)
    @role_required(["Admin"])
    def resolve_all_users(self, info):
        return User.objects.all()

    @role_required(["Waiter"])
    def resolve_private_data(self, info):
        return PrivateData()

class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    assign_role = AssignRole.Field()
    login = LoginMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
