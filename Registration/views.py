from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

import json
import requests
import secrets
import string

from Uni_Socs.models import Universities
from Users.models import LunaUsers
from LUNA_API.settings import DOMAIN_URL


# This app handles the registration flow of a user
# 1. a new user model instance is generated with the associated facebook account/tokens stored there

# 3. the api recieves the uni selection back
# 4. this api then updates the user model with a foreign key of the user's university
# 5. this api then sends to the front end the associated email extension of that uni
# 6. the front end sends back to the api the users university email address
# 7. this api sends a verification email to the user
# 8. the user then follows the verification link which updates the user model as recquired



##################### HELPER METHODS ################################


def send_verification_email(email, verification_key, user_pk):
    email = EmailMessage(
        'LUNA verificaiton',
        f'hello, welcome to LUNA, please click this link to verify your email: {DOMAIN_URL}/register/5/{user_pk}/{verification_key}',
        to=list(email)
    )

    email.send()


def get_profile_picture(uni_id):
    ufi = Universities.objects.filter(id=uni_id).first() # 'ufi'? XD
    profile_picture = requests.get(f'https://graph.facebook.com/v3.0/{ufi.uni_facebook_id}/picture?height=500')

    return profile_picture.url

#####################################################################


# 1.this api sends a list of universities to the front end
def registrations_uni_list(request):
    get_all_from_data_base = Universities.objects.all()
    data = {}
    data['universities'] = []

    # profile picture recieved from graph api here

    for i in get_all_from_data_base:
        data['universities'].append({
            'name': i.name, 'id': i.id, 'profile_picture': get_profile_picture(i.id)
        })

    data_json = json.dumps(data)
    print(data)

    return HttpResponse(data_json)


# 2. the api receives the uni selection back and updates the database accordingly
def user_university_selection(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        uni_id = json_data['uni_selection'][0]['uni_id']
        user_id = json_data['uni_selection'][0]['user']

        selected_uni = Universities.objects.filter(id=uni_id).first()
        user = LunaUsers.objects.filter(id=user_id).first()

        user.uni = selected_uni
        user.save()

        return HttpResponse('reg/2')


# 3. the api then sends to the front end the associated email extension of that uni
def request_university_email_domain(request):
    if request.method == 'POST':
        # recieve the database id of the university whose domain is requested
        json_data = json.loads(request.body)
        uni_id = json_data['email_domain_query'][0]['uni_id']

        # query the database
        uni_domain = Universities.objects.filter(id=uni_id).first().domain

        # prepare json
        data = {}
        data['university_email_domain'] = [{'domain': f'{uni_domain}'}]
        data_json = json.dumps(data)

        # return json
        return HttpResponse(data_json)


# 4. the front end sends back to the api the users university email address
def student_uni_email_input(request):
    if request.method == 'POST':
        # recieve the student email address
        json_data = json.loads(request.body)
        email = json_data['email'][0]['email']
        LunaUserPk = json_data['email'][0]['LunaUser']
        LunaUser = LunaUsers.objects.filter(id=LunaUserPk).first()

        # update the database with email address
        LunaUser.email = email
        LunaUser.save()

        # send verification email
        send_verification_email(email, LunaUser.verification_key, LunaUserPk)

        return HttpResponse('confirm email saved')




def email_verification(request, user_id, verification_key):
    if request.method == 'GET':
        # recieve verification info
        if LunaUsers.objects.filter(verification_key=verification_key).first():
            LunaUser = LunaUsers.objects.filter(id=user_id).first()
            LunaUser.security_key = secrets.token_hex(20)
            # return json to move on to the next part of user registration
        else:
            return HttpResponse('no')

