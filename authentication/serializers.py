from dj_rest_auth.registration.serializers import SocialLoginSerializer


class CustomFacebookLoginSerializer(SocialLoginSerializer):
    def post_signup(self, login, attrs):
        extra_data = login.account.extra_data
        user = login.account.user
        user.email = extra_data.get("id") + "@facebook.com"
        user.name = extra_data.get("name")
        user.save()
