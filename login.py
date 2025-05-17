# Step 1. We begin with creating a Configuration, which contains the username and password for authentication.
import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode

# For optomizing API calls, having this here for safekeeping is much better.
userID = ""

def apiLogin(api_client, configuration):

    # Step 2. VRChat consists of several API's (WorldsApi, UsersApi, FilesApi, NotificationsApi, FriendsApi, etc...)
    # Here we enter a context of the API Client and instantiate the Authentication API which is required for logging in.

    # Instantiate instances of API classes
    auth_api = authentication_api.AuthenticationApi(api_client)

    try:
        # Step 3. Calling getCurrentUser on Authentication API logs you in if the user isn't already logged in.
        current_user = auth_api.get_current_user()
    except UnauthorizedException as e:
        if e.status == 200:
            if "Email 2 Factor Authentication" in e.reason:
                # Step 3.5. Calling email verify2fa if the account has 2FA disabled
                auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(input("Email 2FA Code: ")))
            elif "2 Factor Authentication" in e.reason:
                # Step 3.5. Calling verify2fa if the account has 2FA enabled
                auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(input("2FA Code: ")))
            current_user = auth_api.get_current_user()
        else:
            if e.reason == "Unauthorized":
                print("Try logging in again. Your login credentials may be incorrect\n")
            print("Exception when calling API: %s\n", e)
    except vrchatapi.ApiException as e:
        print("Exception when calling API: %s\n", e)

    print("Logged in as:", current_user.display_name)
    return current_user.id

def apiLogout(api_client):
    # Instantiate instances of API classes
    auth_api = authentication_api.AuthenticationApi(api_client)
    
    auth_api.logout()

# This is no longer used because I grew a brain and realized it doubled the number of API calls.
# I'll leave it here for fun though.
def get_current_user_ID(api_client):
    # Instantiate instances of API classes
    auth_api = authentication_api.AuthenticationApi(api_client)
    user = auth_api.get_current_user()
    id = user.id

    return id