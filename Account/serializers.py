import string
from datetime import timedelta
import random

from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from xml.dom import ValidationErr
from DCRUser.models import CompanyUserRole
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings
from django.utils import timezone

from Account.models import User
from DCR.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from DCRUser.models import CompanyUser, CompanyUserRole


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        ordering = ["-id"]
        model = User
        fields = "__all__"


class UserAddSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=100)
    role_name = serializers.CharField(max_length=100)
    company_name = serializers.CharField(max_length=20)

    class Meta:
        ordering = ["-id"]
        model = User
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
            "address",
            "role_name",
            "company_name",
            "date_of_joining",
        ]

    def create(self, validated_data):
        password = "12345678"
        return User.objects.create_user_with_signal(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            middle_name=validated_data["middle_name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            address=validated_data["address"],
            role_name=validated_data["role_name"],
            company_name=validated_data["company_name"],
            date_of_joining=validated_data["date_of_joining"],
            password=password,
        )


class UserCreationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password didnt matched"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.middle_name = validated_data.get("middle_name")
        instance.email = validated_data.get("email")
        instance.phone_number = validated_data.get("phone_number")
        instance.address = validated_data.get("address")
        instance.date_of_joining = validated_data.get("date_of_joining")
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=250)
    role = serializers.SerializerMethodField("get_role")
    company_id = serializers.SerializerMethodField("get_company_id")
    division_name = serializers.SerializerMethodField("get_division_name")
    company_user_role_id = serializers.SerializerMethodField("get_company_user_role_id")
    company_user_id = serializers.SerializerMethodField("get_company_user_id")
    user_id = serializers.SerializerMethodField("get_user_id")
    company_area_id = serializers.SerializerMethodField("get_company_area_id")

    def get_role(self, data):
        user_id = User.objects.get(email=data["email"])
        if not CompanyUserRole.objects.filter(user_name=user_id).exists():
            return None
        company_user_role_instance = CompanyUserRole.objects.get(user_name=user_id)
        return company_user_role_instance.role_name.role_name.role_name

    def get_company_id(self, data):
        user_id = User.objects.get(email=data["email"])
        if not CompanyUser.objects.filter(user_name=user_id).exists():
            return None
        company_user_instance = CompanyUser.objects.get(user_name=user_id)
        return company_user_instance.company_name.company_id

    def get_division_name(self, data):
        user_id = User.objects.get(email=data["email"])
        if not CompanyUserRole.objects.filter(user_name=user_id).exists():
            return None
        instance = CompanyUserRole.objects.get(user_name=user_id)
        if instance.division_name:
            return instance.division_name.id
        else:
            return None

    def get_company_user_role_id(self, data):
        user_id = User.objects.get(email=data["email"])
        if not CompanyUserRole.objects.filter(user_name=user_id).exists():
            return None
        instance = CompanyUserRole.objects.get(user_name=user_id)
        return instance.id

    def get_company_user_id(self, data):
        user_id = User.objects.get(email=data["email"])
        if not CompanyUser.objects.filter(user_name=user_id).exists():
            return None
        company_user_instance = CompanyUser.objects.get(user_name=user_id)
        return company_user_instance.id

    def get_user_id(self, data):
        user_id = User.objects.get(email=data["email"])
        return user_id.id

    def get_company_area_id(self, data):
        user_id = User.objects.get(email=data["email"])
        company_user_role = CompanyUserRole.objects.get(user_name=user_id)
        if not company_user_role.company_area:
            return None
        return company_user_role.company_area.id

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "role",
            "company_id",
            "division_name",
            "company_user_role_id",
            "company_user_id",
            "user_id",
            "company_area_id",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return validated_data


class UserviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return validated_data


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["password", "confirm_password", "old_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        user = self.context.get("user")
        if user.check_password(attrs.get("old_password")):
            if password == attrs.get("old_password"):
                raise serializers.ValidationError(
                    "Your old password and new password must be different"
                )
            if password != confirm_password:
                raise serializers.ValidationError(
                    "password and confirm password didn't matched"
                )
            else:
                user.set_password(password)
                user.save()
        else:
            raise serializers.ValidationError(
                "Your old password doesnot matches with the password stored in database"
            )
        return attrs


class SendResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]
        model = User

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)

            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token

            # send email
            body = "click following link to reset your password" + link
            data = {"subject": "reset password", "body": body, "to_email": user.email}
            # Util.send_email(data)
            subject = "user reset password"
            message = "Please Change your password"
            email = email
            recipient_list = [email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
            return attrs
        else:
            raise ValidationErr("you are not registered")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "confirm_password"]
        model = User

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        uid = self.context.get("uid")
        token = self.context.get("token")
        if password != confirm_password:
            raise serializers.ValidationError(
                "password and confirm password didnot matched"
            )
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationErr("token is not valid or expired")
        user.set_password(password)
        user.save()
        return attrs


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email not found.")
        otp = generate_otp()

        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        subject = "Password Reset OTP: Secure Your Account"
        message = f"""Dear sir/mam,

             We hope you are doing well.

             We have received a request to reset the password for your easesfa account. To ensure the security of your account, we have generated a one-time password (OTP) for you to use during the password reset process. Your OTP is: {otp}. Please keep this code confidential and do not share it with anyone. This OTP is valid for a limited time and can only be used once to reset your password.

             To proceed with resetting your password, please enter the OTP code provided above when prompted on our website or mobile app.

             If you did not initiate this password reset request, please disregard this email and take necessary precautions to secure your account.

             Thank you for your cooperation in maintaining the security of your easesfa account. If you encounter any issues or need further assistance, please feel free to reach out to our support team at support@thinkfortech.com.
             
             Best regards,
             easeSFA Team"""
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

    def validate_otp(self, value):
        email = self.initial_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

        if user.otp != value:
            raise serializers.ValidationError("Invalid OTP.")

        expiration_time = user.otp_created_at + timedelta(minutes=3)
        if timezone.now() > expiration_time:
            raise serializers.ValidationError("OTP has expired.")

        user.otp = None
        user.otp_created_at = None
        user.save()

        return value

    def create(self, validated_data):
        email = validated_data["email"]
        new_password = validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        user.set_password(new_password)
        user.save()

        return validated_data


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        expiration_time = user.otp_created_at + timedelta(minutes=5)
        if timezone.now() > expiration_time:
            raise serializers.ValidationError("OTP has expired.")
        return data


class ResetPasswordOtp(serializers.Serializer):
    pass


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
