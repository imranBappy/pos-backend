import datetime
import decimal

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# ThirdParty Library Import
from easy_thumbnails.fields import ThumbnailerImageField
from multiselectfield import MultiSelectField

from app.bases.constant import PanelTypeChoices
from app.bases.models import BaseModel, BaseWithoutID
from app.bases.utils import (
    build_absolute_uri,
    create_token,
    email_validator,
    promo_code_validator,
    username_validator,
)
from app.crm.choices import AdvertiseStatusChoice, CurrencyChoice

from .choices import (
    AgreementChoices,
    CareerLevelChoice,
    DeviceTypeChoices,
    EducationLevelChoice,
    EmploymentTypeChoice,
    GenderChoices,
    JobSectionChoice,
    NoticePeriodChoice,
    SalaryRangeChoice,
    SocialAccountTypeChoices,
    VisaStatusChoice,
    WorkExperienceChoice,
)
from .managers import (
    UserAccessTokenManager,
    UserDeviceTokenManager,
    UserManager,
    UserOTPManager,
    UserPasswordResetManager,
    UserSocialAccountManager,
)
from .tasks import send_email_on_delay


def content_logo_name(instance, filename):
    return f"{settings.AWS_STORAGE_BUCKET_FOLDER}/client_{instance.id}/logo/{filename}"


def content_cover_name(instance, filename):
    return f"{settings.AWS_STORAGE_BUCKET_FOLDER}/client_{instance.id}/cover_photo/{filename}"


class ClientDetails(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slogan = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    logo = ThumbnailerImageField(
        'ClientLogo',
        upload_to=content_logo_name,
        blank=True,
        null=True
    )
    cover_photo = ThumbnailerImageField(
        'ClientCoverPhoto',
        upload_to=content_cover_name,
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)
    formation_date = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_client_details"  # define table name for database
        verbose_name_plural = 'Client Details'

    def __str__(self) -> str:
        return str(self.name)


def content_file_name(instance, filename):
    return f"{settings.AWS_STORAGE_BUCKET_FOLDER}/{instance.id}/profile/{filename}"


def content_file_name_document(instance, filename):
    return f"{settings.AWS_STORAGE_BUCKET_FOLDER}/{instance.id}/document/{filename}"


class User(BaseWithoutID, AbstractBaseUser, PermissionsMixin):
    """Store custom user information.
    all fields are common for all users."""
    username = models.CharField(
        max_length=30,
        validators=[username_validator],
        unique=True,
        null=True
    )  # unique user name to perform username password login.
    first_name = models.CharField(
        max_length=150, null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=150, null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=100,
        validators=[email_validator],
        unique=True
    )  # unique email to perform email login and send alert mail.

    # Verification Check
    is_verified = models.BooleanField(
        default=False
    )
    is_email_verified = models.BooleanField(
        default=False
    )
    is_phone_verified = models.BooleanField(
        default=False
    )
    is_profile_photo_verified = models.BooleanField(
        default=False
    )
    rejection_reason_profile_photo = models.TextField(
        blank=True,
        null=True
    )
    is_cv_verified = models.BooleanField(
        default=False
    )
    rejection_reason_cv = models.TextField(
        blank=True,
        null=True
    )
    term_and_condition_accepted = models.BooleanField(
        default=False
    )
    privacy_policy_accepted = models.BooleanField(
        default=False
    )

    # permission
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )  # main man of this application.
    is_deleted = models.BooleanField(
        default=False
    )
    deleted_on = models.DateTimeField(
        null=True,
        blank=True
    )
    deleted_phone = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True
    )

    # details
    last_active_on = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    activation_token = models.UUIDField(
        blank=True,
        null=True
    )
    deactivation_reason = models.TextField(
        null=True,
        blank=True
    )
    is_expired = models.BooleanField(
        default=False
    )  # this flag will define user delete stop this all token for a while

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Enter Phone number with country code"
    )  # phone number validator.
    phone = models.CharField(
        _("phone number"),
        validators=[phone_regex],
        max_length=15,
        unique=True,
        null=True,
        # blank=True
    )
    is_phone_visible = models.BooleanField(default=True)
    gender = models.CharField(
        max_length=8,
        choices=GenderChoices.choices,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    # Profile Picture
    photo = ThumbnailerImageField(
        'ProfilePicture',
        upload_to=content_file_name,
        blank=True,
        null=True
    )
    photo_uploaded_at = models.DateTimeField(
        blank=True,
        null=True
    )
    cv = models.FileField(
        upload_to=content_file_name_document,
        blank=True,
        null=True
    )  # if user have any cv attached
    # current_city = models.ForeignKey(
    #     'crm.city',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )
    # nationality = CountryField(blank=True, null=True)  # store candidate country belongs to
    nationality = models.ForeignKey(
        'core.Country', on_delete=models.SET_NULL, blank=True, null=True)  # store candidate country belongs to
    career_level = models.CharField(max_length=32, choices=CareerLevelChoice.choices, blank=True,
                                    null=True)  # career level of employee
    # work_experience = models.CharField(max_length=64, choices=WorkExperienceChoice.choices, blank=True,
    #                                    null=True)  # work experience in years
    education_level = models.CharField(_('Highest education'), max_length=32, choices=EducationLevelChoice.choices,
                                       blank=True, null=True)  # educational degree of employee
    salary_range = models.CharField(max_length=32, choices=SalaryRangeChoice.choices,
                                    blank=True, null=True)  # salary range of expectation
    currency = models.CharField(max_length=5, choices=CurrencyChoice.choices, blank=True, null=True,
                                default=CurrencyChoice.ETB)  # define in which currency used
    current_position = models.CharField(max_length=32, blank=True, null=True)  # store user current position
    current_company = models.CharField(max_length=32, blank=True, null=True)  # store user current company working on
    commitment = models.CharField(max_length=32, choices=EmploymentTypeChoice.choices, blank=True,
                                  null=True)  # if user have any commitment
    notice_period = models.CharField(max_length=32, choices=NoticePeriodChoice.choices, blank=True,
                                     null=True)  # when to notice for job
    visa_status = models.CharField(max_length=32, choices=VisaStatusChoice.choices, blank=True, null=True,
                                   default=VisaStatusChoice.NOT_APPLICABLE)  # what type of visa needed
    sap_customer_id = models.CharField(max_length=6, null=True, blank=True)
    panel_type = MultiSelectField(choices=PanelTypeChoices.choices, null=True)  # respective panel info to be stored

    # last login will provide by django abstract_base_user.
    # password also provide by django abstract_base_user.

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = f"{settings.DB_PREFIX}_users"  # define table name for database
        ordering = ['-created_on']  # define default filter as created in descending

    def __str__(self) -> str:
        return str(self.email)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def send_email_verification(self, host):
        self.activation_token = create_token()
        self.is_email_verified = False
        self.save()
        context = {
            'username': self.username,
            'email': self.email,
            'url': build_absolute_uri(f"email-verification/?token={self.activation_token}", host),
        }
        template = 'emails/sing_up_email.html'
        subject = 'Email Verification'
        send_email_on_delay.delay(template, context, subject, self.email)  # will add later for sending verification

    @property
    def is_admin(self) -> bool:
        return self.is_staff or self.is_superuser

    @property
    def is_driver(self) -> bool:
        from app.core.choices import EmployeeStatusChoice
        emp = getattr(self, 'presell_employee', None)
        if emp and emp.designation == EmployeeStatusChoice.DRIVER:
            return True
        else:
            return False

    @property
    def live_advertise_count(self) -> int:
        try:
            return self.posted_advertises.filter(
                availability=True, status=AdvertiseStatusChoice.APPROVED, is_deleted=False,
                expiry_date__gt=timezone.now().today()
            ).count()
        except Exception:
            return 0

    @property
    def status(self) -> str:
        status = "active"
        if self.is_deleted:
            status = "deleted"
        elif self.is_active and not self.deactivation_reason:
            status = "active"
        elif not self.is_active and not self.deactivation_reason:
            status = "blocked"
        elif not self.is_active and self.deactivation_reason:
            status = "deactivated"
        return status

    @property
    def cv_status(self):
        status = "no_data"
        if (
            self.cv
            and not self.is_cv_verified
            and not self.rejection_reason_cv
        ):
            status = "pending"
        elif (
            not self.is_cv_verified
            and self.rejection_reason_cv
        ):
            status = "rejected"
        elif self.is_cv_verified:
            status = "approved"
        return status

    @property
    def image_status(self):
        status = "no_data"
        if (
            self.photo
            and not self.rejection_reason_profile_photo
            and not self.is_profile_photo_verified
        ):
            status = "pending"
        elif (
            self.photo
            and self.is_profile_photo_verified
            and not self.rejection_reason_profile_photo
        ):
            status = "approved"
        elif (
            self.photo
            and self.rejection_reason_profile_photo
        ):
            status = "rejected"
        return status

    @property
    def is_supervisor(self):
        if getattr(self, 'supervisor', None):
            return True
        return False

    @property
    def is_merchandiser(self):
        if getattr(self, 'merchandiser', None):
            return True
        return False


class UserSkill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_skills"
    )  # skilled user
    industry = models.CharField(
        max_length=32,
        choices=JobSectionChoice.choices
    )  # category industry of experience
    work_experience = models.CharField(
        max_length=64,
        choices=WorkExperienceChoice.choices,
        default=WorkExperienceChoice.NO_EXPERIENCE
    )  # work experience in years

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_skills"  # define table name for database
        unique_together = ("user", "industry", "work_experience")


class UnitOfHistory(models.Model):
    """We will create log for every action
    those data will store in this model"""

    action = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )  # in this field we will define which action was perform.
    created = models.DateTimeField(
        auto_now_add=True
    )
    old_meta = models.JSONField(
        null=True
    )  # we store data what was the scenario before perform this action.
    new_meta = models.JSONField(
        null=True
    )  # we store data after perform this action.
    header = models.JSONField(
        null=True
    )  # request header that will provide user browser
    # information and others details.
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="performer"
    )  # this user will be action performer.
    perform_for = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="perform_for"
    )  # sometime admin/superior  will perform some
    # specific action for employee/or user e.g. payroll change.
    # Generic Foreignkey Configuration. DO NOT CHANGE
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.CharField(
        max_length=100
    )
    content_object = GenericForeignKey()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_unit_of_histories"  # define database table name
        ordering = ['-created']  # define default order as created in descending

    def __str__(self) -> str:
        return self.action or "action"

    @classmethod
    def user_history(
        cls,
        action,
        user,
        request,
        new_meta=None,
        old_meta=None,
        perform_for=None
    ) -> object:
        try:
            data = {i[0]: i[1] for i in request.META.items() if i[0].startswith('HTTP_')}
        except BaseException:
            data = None
        cls.objects.create(
            action=action,
            user=user,
            old_meta=old_meta,
            new_meta=new_meta,
            header=data,
            perform_for=perform_for,
            content_type=ContentType.objects.get_for_model(User),
            object_id=user.id
        )


class ResetPassword(models.Model):
    """
    Reset Password will store user data
    who request for reset password.
    TODO:: have to set expired time in future.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    token = models.UUIDField()

    objects = UserPasswordResetManager()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_password_reset"
        ordering = ['-id']  # define default order as id in descending


class UserDeviceToken(BaseModel):
    """
    To Tiggerd FMC notification we need
    device token will store user device token
    to triggered notification.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='device_tokens'
    )
    device_token = models.CharField(
        max_length=200
    )
    device_type = models.CharField(
        max_length=8,
        choices=DeviceTypeChoices.choices
    )
    mac_address = models.CharField(max_length=48, null=True)
    is_current = models.BooleanField(default=False)
    objects = UserDeviceTokenManager()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_device_tokens"
        ordering = ['-created_on']  # define default order as created in descending

    def save(self, *args, **kwargs):
        super(UserDeviceToken, self).save(*args, **kwargs)
        if self.is_current:
            self.user.device_tokens.filter(is_current=True).exclude(id=self.id).update(is_current=False)
        if UserDeviceToken.objects.filter(device_token=self.device_token):
            UserDeviceToken.objects.filter(device_token=self.device_token).exclude(id=self.id).delete()


class UserSocialAccount(BaseWithoutID):
    """Social Account will store will
    type id and for whom."""

    social_id = models.CharField(
        max_length=100
    )
    social_type = models.CharField(
        max_length=20,
        choices=SocialAccountTypeChoices.choices
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    objects = UserSocialAccountManager()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_social_accounts"  # define database table name
        unique_together = (("user", "social_type"),)  # define two field unique together
        ordering = ['-created_on']  # define default order as created in descending


# class OnlineUser(models.Model):
#     """
#         Store information if user is online or not
#     """
#
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="online_status"
#     )
#     is_online = models.BooleanField(default=False)
#     last_seen = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.user}: {self.is_online} // {self.last_seen}"
#
#     class Meta:
#         db_table = f"{settings.DB_PREFIX}_online_users"  # define database table name
#         ordering = ['-last_seen']  # define default order as last_seen in descending


class UserOTP(models.Model):
    """
        Store information for user otp verification
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_otp"
    )  # user who is responsible for
    otp = models.CharField(max_length=6)  # exact value of one time pin
    created_on = models.DateTimeField(
        auto_now_add=True
    )  # object creation time. will automatically generate
    updated_on = models.DateTimeField(
        auto_now=True
    )  # object update time. will automatically generate

    objects = UserOTPManager()

    def __str__(self):
        return f"{self.user.email}: {self.otp}"

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_otps"  # define database table name
        ordering = ['-updated_on']  # define default order as updated_on in descending
        unique_together = ("user", "otp")  # make user and otp unique together


class Agreement(BaseWithoutID):
    data = models.TextField(
        blank=True
    )
    type_of = models.CharField(
        max_length=20,
        choices=AgreementChoices.choices,
    )
    agreement_for = models.CharField(
        default=PanelTypeChoices.B2B,
        max_length=20,
        choices=PanelTypeChoices.choices,
        blank=True,
        null=True
    )

    class Meta:
        db_table = f"{settings.DB_PREFIX}_agreements"
        unique_together = ("type_of", "agreement_for")


class ContactPurpose(BaseWithoutID):
    title = models.CharField(max_length=128, unique=True)
    message = models.TextField(
        blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_contact_purposes"


class ContactUs(BaseWithoutID):
    email = models.EmailField(
        max_length=128,
        validators=[email_validator]
    )
    subject = models.CharField(max_length=128)
    description = models.TextField()
    inquiry = models.ForeignKey(ContactPurpose, on_delete=models.DO_NOTHING, blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_contact_us"
        verbose_name_plural = "Contact us"
        ordering = ["-created_on"]

    @property
    def user(self):
        try:
            return User.objects.get(email=self.email)
        except User.DoesNotExist:
            return None


class PromoCode(BaseWithoutID):
    FLAT = "flat"
    PERCENTAGE = "percentage"
    TYPE_CHOICES = (
        (FLAT, "flat"),
        (PERCENTAGE, "percentage")
    )

    name = models.CharField(
        max_length=100, unique=True, validators=[promo_code_validator])
    promo_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    max_uses_limit = models.PositiveIntegerField(default=1)
    max_limit_per_user = models.PositiveIntegerField(default=1)
    value = models.PositiveIntegerField()
    min_amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_promo_codes"

    @classmethod
    def get_active_promo_filter(cls):
        today = timezone.now().date()
        filter_q = models.Q(is_active=True, start_date__lte=today, end_date__gte=today)
        return filter_q

    @classmethod
    def get_active_promo_codes_for_user(cls, user, promo_code):
        now = timezone.now()
        today = timezone.now().date()
        promo_delta_time = timezone.now() - datetime.timedelta(minutes=settings.PROMO_DELTA_MINUTES)
        # filter_q = models.Q(is_payment_success=True) | models.Q(is_payment_success=False,
        #                                                         created_on__range=(promo_delta_time, now))
        filter_q = models.Q(created_on__range=(promo_delta_time, now))
        used_count = user.used_promo_codes.filter(
            promo_code__name=promo_code).filter(filter_q).count()
        total_count = UserPromoCode.objects.filter(promo_code__name=promo_code).filter(filter_q).count()
        return cls.objects.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
            max_limit_per_user__gt=used_count,
            max_uses_limit__gt=total_count
        ).get(name=promo_code)

    @classmethod
    def get_promo_and_apply(cls, user, promo_code, price):
        if not promo_code:
            return None, None, price
        try:
            promo_obj = cls.get_active_promo_codes_for_user(user, promo_code)
            price = decimal.Decimal(price)
            if promo_obj.min_amount > price:
                raise ValidationError(f"Min amount to apply this promo code is {promo_obj.min_amount}.")
            if promo_obj.max_amount and price > promo_obj.max_amount:
                raise ValidationError(
                    f"Max amount for which this promo code can be applied is {promo_obj.max_amount}.")

            return promo_obj, *promo_obj.get_discounted_price(price)
        except cls.DoesNotExist:
            raise ValidationError(settings.PROMO_CODE_ERROR_MESSAGE)
        except ValidationError as e:
            raise e

    def get_discounted_price(self, price):
        price = decimal.Decimal(price)
        if self.promo_type == self.FLAT:
            amount_discounted = self.value if self.value < price else price
        else:
            amount_discounted = round((price * decimal.Decimal(self.value / 100)), 2)
        return amount_discounted, price - amount_discounted

    def __str__(self):
        return f"{self.name} : {self.promo_type} - {self.value}"


class UserPromoCode(BaseWithoutID):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="used_promo_codes"
    )
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_payment_success = models.BooleanField(default=False)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_promo_codes"


class CancellationReason(models.Model):
    title = models.CharField(max_length=128, unique=True)
    message = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_cancellation_reasons"

    def __str__(self):
        return f"{self.title}"


class TrackUserLogin(BaseWithoutID):
    username = models.CharField(
        max_length=30, null=True
    )
    email = models.EmailField(
        max_length=100, null=True
    )
    data = models.JSONField(
        null=True
    )  # we store data after perform this action.
    header = models.JSONField(
        null=True
    )  # request header that will provide user browser
    is_success = models.BooleanField(default=False)

    class Meta:
        db_table = f"{settings.DB_PREFIX}_user_login_tracks"  # define table name for database
        ordering = ['-created_on']  # define default order as created in descending


class AccessToken(BaseWithoutID):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='access_tokens'
    )
    token = models.TextField()
    mac_address = models.CharField(max_length=48, null=True)

    objects = UserAccessTokenManager()

    class Meta:
        db_table = f"{settings.DB_PREFIX}_access_tokens"  # define table name for database
        ordering = ['-created_on']  # define default order as created in descending
