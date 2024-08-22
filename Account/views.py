from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import jwt
from Account.serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LogoutSerializer,
    OTPVerificationSerializer,
    ResetPasswordSerializer,
    SendResetPasswordEmailSerializer,
    UserAddSerializer,
    UserCreationSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserProfileSerializer,
    UserSerializers,
)
from DCR.settings import SECRET_KEY
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from DCRUser.models import CompanyUserRole

from .models import User
from .pagination import CustomPagination


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserCreationView(APIView):
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                data={"token": token, "msg": "User Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if User.objects.filter(email=request.data.get("email")).exists():
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get("email")
                password = serializer.data.get("password")
                role = serializer.data.get("role")
                company_id = serializer.data.get("company_id")
                division = serializer.data.get("division_name")
                company_user_role_id = serializer.data.get("company_user_role_id")
                company_user_id = serializer.data.get("company_user_id")
                user_id = serializer.data.get("user_id")
                company_area_id = serializer.data.get("company_area_id")
                is_highest_priority = serializer.data.get("is_highest_priority")
                if email is None or password is None:
                    return Response(
                        data={"No email or password!!!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if role is None or company_user_role_id is None:
                    return Response(
                        data={"The user have no role in any company!!!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if company_id is None or company_user_id is None:
                    return Response(
                        data={"The user is not registered with any company!!!!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user = authenticate(email=email, password=password)
                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response(
                        data={
                            "token": token,
                            "status": "success",
                            "role": role,
                            "company_id": company_id,
                            "company_division_name": division,
                            "company_user_role_id": company_user_role_id,
                            "company_user_id": company_user_id,
                            "user_id": user_id,
                            "company_area_id": company_area_id,
                            "is_highest_priority": is_highest_priority,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        data={"Email or Password is not valid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                data={"Email doesnot exists"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginByIdView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get("user_id")
            password = serializer.data.get("password")
            role = serializer.data.get("role")
            company_id = serializer.data.get("company_id")
            division = serializer.data.get("division_name")
            company_user_role_id = serializer.data.get("company_user_role_id")
            company_user_id = serializer.data.get("company_user_id")
            company_area_id = serializer.data.get("company_area_id")
            is_highest_priority = serializer.data.get("is_highest_priority")
            
            if user_id is None or password is None:
                return Response(
                    {"detail": "No user ID or password provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"detail": "User ID does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = authenticate(username=user.username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "status": "success",
                        "role": role,
                        "company_id": company_id,
                        "company_division_name": division,
                        "company_user_role_id": company_user_role_id,
                        "company_user_id": company_user_id,
                        "user_id": user_id,
                        "company_area_id": company_area_id,
                        "is_highest_priority": is_highest_priority,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_classes = CustomPagination

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                data={"password changed successfully"}, status=status.HTTP_200_OK
            )


class ResetPasswordEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                data={"reset password sent to the email, please check your email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                data={"password reset successful"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_admin"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
            serializer.save()
        except Exception as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "create":
            return UserAddSerializer
        else:
            return UserSerializers


class UserLogout(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT, data="User logged out successfully"
        )


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"OTP sent to your email address."}, status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                data={"OTP verified successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"Password reset successfully."}, status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def get_user_details_from_token(request):
    access = request.data.get("access")
    decrypted_access_token = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
    user_id = decrypted_access_token.get("user_id")
    company_user_instance = CompanyUserRole.objects.get(user_name=user_id)
    data = {"company_user_role_id": company_user_instance.id}
    return JsonResponse(data, status=201, headers={"content_type": "application/json"})


@api_view(["POST"])
def check_refresh_token(request):
    refresh_token = request.data.get("refresh")
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

    # check the payload to ensure that the token is valid
    if "user_id" in payload:
        data = {"status": "valid"}
        return JsonResponse(
            data, status=201, headers={"content_type": "application/json"}, safe=False
        )
    else:
        data = {"status": "invalid"}
        return JsonResponse(
            data, status=401, headers={"content_type": "application/json"}, safe=False
        )
    # do something with the user ID, e.g. retrieve the user object
