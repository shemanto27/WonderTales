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
    callback_url = "https://chef-starz.com/auth/apple/callback/"
    client_class = OAuth2Client
