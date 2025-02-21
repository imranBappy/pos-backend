import graphene
from django.contrib.auth.models import Group
from django.db import transaction
from apps.accounts.models import User as CustomUser, UserOTP, UserRole, Address,Building
from apps.accounts.objectType import UserType, AddressType
from graphql import GraphQLError
from backend.authentication import TokenManager, isAuthenticated
from apps.accounts.forms import UserForm, AddressForm, BuildingForm
from django.conf import settings
from graphene_django.forms.mutation import DjangoFormMutation
from apps.base.utils import  create_graphql_error, generate_otp, get_object_or_none

base_url = settings.WEBSITE_URL

class RegisterUser(graphene.Mutation):
    """
        This mutation will be for end customer
    """
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String(required=False)

    success = graphene.Boolean()
    message = graphene.String()
    id = graphene.ID()

    @transaction.atomic
    def mutate(self, info, name, email,password, phone=None):
        email = email.lower()
        find_user = get_object_or_none(CustomUser, email=email)
        if find_user is not None:
            raise GraphQLError(message="Email is already registered.")
        
        if phone:
            find_by_phone_user = get_object_or_none(CustomUser, phone=phone)
            if find_by_phone_user is not None:
                raise GraphQLError(message="Phone is already registered.")
        
        user = CustomUser.objects.create_user(
            name=name, email=email, password=password, phone=phone
        )
        role = Group.objects.get(name="CUSTOMER")
        user.is_verified = False  
        user.role  = role
        user.save()
        gen_otp = generate_otp()
        user.send_email_verification(
            gen_otp, base_url
        )
        new_otp=UserOTP(user=user, otp=gen_otp)
        new_otp.save()
        return RegisterUser(success=True, message="Registration successful!", id=user.id)

class OTPVerification(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    
    class Arguments:
        email = graphene.String()
        otp = graphene.String()
    
    def mutate(self, info, email, otp, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise GraphQLError(
                message="Not Found User",
            )
        
        if user.is_verified:
            raise GraphQLError(message="You are already verified.")
        
        user_otp = UserOTP.objects.check_otp(otp=otp, user=user)
        
        if user_otp and user.is_active:
            user.is_verified = True
            user.save()
        else:
            raise GraphQLError(message="OTP is invalid or expired")
            
        return OTPVerification(
            success=True,
            message='User account is successfully verified',
            user = user
        )
class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    @staticmethod
    def mutate(root, info, email, password):
        try:
            
            if not email:
                return GraphQLError("Invalid email or password.",)
            user = CustomUser.objects.get(email=email.lower()) 

            if not user.check_password(password):
                return  GraphQLError("Invalid email or password.")
            if not user.is_active:
                return  GraphQLError("Account is inactive.")
            
            payload = {
                'name' : user.name,
                'email': user.email,
                'role': user.role.name if user.role else UserRole.ADMIN if user.is_superuser else UserRole.CUSTOMER,
                'photo': user.photo
            }
            token = TokenManager.get_access(payload)
            return LoginUser(token=token,user=user, success=True, message="Login successful.")
        except CustomUser.DoesNotExist:
            print("user dose not exit")
            return  GraphQLError("Invalid email or password.",)
       
class PasswordResetMail(graphene.Mutation):
    message = graphene.String()
    success  = graphene.Boolean()
    
    class Arguments:
        email = graphene.String(required=True)
    
    def mutate(self, info, email):
        user = CustomUser.objects.get(email=email)
        otp = UserOTP.objects.get_object_or_none(user = user.id)
        if not otp:
            generated_top = generate_otp()
            otp = UserOTP(user=user, otp=generated_top)
            otp.save()
        
        verification_link = f"{base_url}/reset-password?otp={otp.otp}&email={user.email}"
        user.send_email_verification(otp.otp, verification_link)
        return PasswordResetMail(
            message='Successfully send mail',
            success=True
        )

class PasswordReset(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    
    class Arguments:
        email = graphene.String(required=True)
        otp = graphene.String(required=True)
        password = graphene.String(required=True)
    
    def mutate(self, info, email, otp, password):
        
        user =  CustomUser.objects.get(email=email)
        if UserOTP.objects.check_otp(otp=otp, user=user.id) == False:
            return GraphQLError(message="OTP is invalid!")

        user.set_password(password)
        user.save()
        
        return PasswordReset(message="Password reset success", success=True)
    
class PasswordChange(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()
    
    class Arguments:
        password = graphene.String()
        new_password = graphene.String()
    
    @isAuthenticated()
    def mutate(self, info, password, new_password):
        user = info.context.user
        if not user.check_password(password):
            raise GraphQLError(
                message="Wrong password",
                extensions={
                    "message": "Wrong password",
                    "code": "wrong_password"
                }
            )
        user.set_password(new_password)
        user.save()
        return PasswordChange(
            success=True,
            message="Password change successful"
        )


class ProfileUpdate(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    profile = graphene.Field(UserType)
    
    class Meta:
        form_class = UserForm
    
    @isAuthenticated()
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(CustomUser, id=input.get('id'))
        if not instance:
            raise GraphQLError("User not found!")
        form = UserForm(input, instance=instance)
        role = input.get("role")
        
        if role and not info.context.User.is_superuser and int(role) != instance.role.id:
            raise GraphQLError("You can't update role.")
        if not form.is_valid():
            print(form.errors)
            create_graphql_error(form)
        
        profile = form.save()
        return ProfileUpdate(message="Update profile!", success=True, profile=profile)
                
class AddressCUD(DjangoFormMutation):
    success = graphene.Boolean()
    address = graphene.Field(AddressType)
    class Meta:
        form_class = AddressForm

    @isAuthenticated()
    def mutate_and_get_payload(self, info, **input):
         
        id=input.get('id')
        user = input.get('user')
        
        address_type = input.get('address_type')
        instance = get_object_or_none(Address, id=id, address_type=address_type)
         
        if not instance:
           instance = get_object_or_none(Address, user=user, address_type=address_type)
        
        # if is it First address then it will be default
        if not id:
            allAddress  = Address.objects.filter(user=user)
            if not  allAddress:
                input['default'] = True
                
        
        form = AddressForm(input, instance=instance)
        if form.is_valid():
            address = form.save()
            return AddressCUD( success=True, address=address)
        
        create_graphql_error(form)


class AddressUpdate(graphene.Mutation):
    success = graphene.Boolean()
    # address = graphene.Field(AddressType)
    
    class Arguments:
        user = graphene.ID(required=True)
        address_type = graphene.String()
        
    def mutate(self,info, user, address_type):
        address = Address.objects.get(user=user, address_type=address_type)
        if(address.default):
            return AddressUpdate(success=True)
        
        if address_type=='HOME':
            address = Address.objects.get(user=user, address_type='OFFICE')
            if(address):
                if(address.default):
                    address.default = False
                    address.save()
        
        if address_type=='OFFICE':
            address = Address.objects.get(user=user, address_type='HOME')
            if(address):
                if(address.default):
                    address.default = False
                    address.save()
        
        address = Address.objects.get(user=user, address_type=address_type)
        address.default = True
        address.save()
        
        return AddressUpdate(success=True)
        
        
        

class BuildingCUD(DjangoFormMutation):
    success = graphene.Boolean()
    id = graphene.ID()
    
    class Meta:
        form_class = BuildingForm
    @isAuthenticated()
    def mutate_and_get_payload(self, info, **input):
        addressId=input.get('address')
        id = input.get('id')
        
        instance = get_object_or_none(Building, id=id)   
        form = BuildingForm(input, instance=instance)
        
        if not form.is_valid():
            create_graphql_error(form)
        
        addressInstance = get_object_or_none(Address, id=addressId)
        if not addressInstance:
           raise GraphQLError("Address not found!")
            
        building = form.save()
        return BuildingCUD( success=True, id=building.id)


class Mutation(graphene.ObjectType):
    
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    otp_verify = OTPVerification.Field()
    password_reset_mail = PasswordResetMail.Field()
    password_reset = PasswordReset.Field()
    password_change = PasswordChange.Field()
    profile_update = ProfileUpdate.Field()
    address_cud = AddressCUD.Field()
    building_cud = BuildingCUD.Field()
    address_update = AddressUpdate.Field() 
    