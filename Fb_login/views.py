from django.shortcuts import render
from django.http import HttpResponse

from Users.models import LunaUsers
from Fb_login.models import Access_Tokens

import requests, secrets, json

from LUNA_API.settings import CLIENT_ID, DOMAIN_URL, SCOPE, REDIRECT_URI, FULL_LOGIN_URL

# This app is to handle the facebook oauth, handling of facebook access tokens and to check
# if the user is registered or not.
# (if already registered, normal login flow - if not registered, triggers registration flow)


def register_new_user(id_facebook, username_facebook_array, access_token):
    # 1. make the new LunaUser object
    first_name = username_facebook_array[0]
    last_name = username_facebook_array[1]
    fb_id = id_facebook
    
    new_LunaUser = LunaUsers.objects.create(first_name=first_name, last_name=last_name, fb_id=fb_id, security_key=None,
                                            verification_key=secrets.token_hex(15))

    Access_Tokens.objects.create(User=new_LunaUser, access_token=access_token)

    data = {}
    data['new_LunaUser'] = []
    data['new_LunaUser'].append({
        'LunaUserId':new_LunaUser.id,
        })

    response_data = json.dumps(data)

    return HttpResponse(response_data)


    # SEND TO CORONA LUNAUSER ID AND SIGNAL TO TRIGGER REGISTRATION SEQUENCE

    # everywhere is looking for the user's secret key - the secret key is None until email verification is complete.

    # email verification ********************


def login(request):
    return render(request, 'Fb_login/login.html')


def login_success(request):
    #
    # 1.get the access token FROM CORONA
    #
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)

        # get the at
        access_token = json_data['at']


    #
    # 2. get the firstname, lastname and facebok id
    #
    id_from_access_token_request = requests.get(f'https://graph.facebook.com/v3.0/me?fields=id,name&access_token={access_token}').json()

    id_facebook = id_from_access_token_request['id']
    username_facebook = id_from_access_token_request['name']

    username_facebook_array = username_facebook.split()

    #
    # 3.check if user is already a registered LunaUser or not
    #
    if LunaUsers.objects.filter(fb_id=id_facebook).exists():

        user = LunaUsers.objects.filter(fb_id=id_facebook).first()

        token = Access_Tokens.objects.filter(User=user).first()
        token.access_token = access_token
        token.save()

        security_key = secrets.token_hex(20)
        user.security_key = security_key
        user.save() # generated in api then saved on the phone

        # SEND BACK TO CORONA LunaUserId and security_key

        data = {}
        data['existing_LunaUser'] = []
        data['existing_LunaUser'].append({
            'LunaUserId':user.id,
            'security_key':user.security_key,
            })

        response_data = json.dumps(data)

        return HttpResponse(response_data)

    else:

        #
        # 4. create a new user and attach the access token
        #
       
        return register_new_user(id_facebook, username_facebook_array, access_token)
    


# logout is handled in the front end
# every user has a secret key applied to them
# the secret key is held on the device itself - upon launch the secret key is queried against the db and a match is verified
# login automatically occurs
# when logout is called on the device the secret key is deleted
# if a user is logged out, there is no secret key, facebook login dialogue appears instead

    


