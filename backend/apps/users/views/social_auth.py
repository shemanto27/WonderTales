from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    """
    Google Login API endpoint.
    Flutter developer should send the 'access_token' or 'id_token' received from Google.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/auth/google/callback/" 
    client_class = OAuth2Client

class AppleLogin(SocialLoginView):
    """
    Apple Login API endpoint.
    Flutter developer should send the 'access_token' or 'id_token' received from Apple.
    """
    adapter_class = AppleOAuth2Adapter
    callback_url = "https://wonder-tales.com/auth/apple/callback/"
    client_class = OAuth2Client

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUserModel = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class FlutterGoogleLoginView(APIView):
    """
    Custom Google login that only takes email to match the flutter dev's requirements.
    WARNING: Accepting only an email without an id_token is insecure and can allow 
    impersonation. Use with caution.
    """
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"success": False, "error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = CustomUserModel.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.is_email_verified = True
            user.username = email.split('@')[0]
            user.save()
            
        tokens = get_tokens_for_user(user)
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.username or email.split('@')[0],
            "profile_image": request.build_absolute_uri(user.user_image.url) if user.user_image else "https://prommt.cc/profile_images/default_avatar.png"
        }
        
        return Response({
            "success": True,
            "created": created,
            "refresh": tokens['refresh'],
            "access": tokens['access'],
            "user": user_data
        })

class FlutterAppleLoginView(APIView):
    """
    Custom Apple login that takes id_token and email.
    """
    permission_classes = []

    def post(self, request):
        id_token = request.data.get('id_token')
        email = request.data.get('email')
        
        if not id_token:
            return Response({"success": False, "error": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not email:
            return Response({"success": False, "error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        user, created = CustomUserModel.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.is_email_verified = True
            user.username = email.split('@')[0]
            user.save()
            
        tokens = get_tokens_for_user(user)
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.username or email.split('@')[0],
            "profile_image": request.build_absolute_uri(user.user_image.url) if user.user_image else "https://prommt.cc/profile_images/default_avatar.png"
        }
        
        return Response({
            "success": True,
            "created": created,
            "refresh": tokens['refresh'],
            "access": tokens['access'],
            "user": user_data
        })
