from django.test import TestCase
from django.urls import reverse

from Uni_Socs.models import Universities
from Users.models import LunaUsers

import json


class Registration_Tests(TestCase):
    #
    #   SetUp For Test
    #
    def setUp(self):
        LunaUsers.objects.create(first_name='Roman', last_name='Synovets', fb_id='736587236532735')

        Universities.objects.create(name='Ziferblat_University', uni_facebook_id='ClockfaceKiev')
        Universities.objects.create(name='Oxford')


    #
    # a user is shown all the universities to choose
    # when registration starts at /register/1 all the universities are sent as a json signal to the front end
    #
    def test_when_registration_start_and_user_show_all_universities_for_choose(self):
        response = self.client.get(reverse('universities_list'), follow=True)       # NEED FIXING (Need JSON)

        get_all_from_uni = Universities.objects.all()

        for i in get_all_from_uni:
            self.assertIn(i.name, str(response.content, encoding='utf8'))
            self.assertIn(str(i.id), str(response.content, encoding='utf8'))

    # the user selects which university they attend
    # when the university choice is sent to /register/2 the user model is updated to show the user's university
    def test_user_model_updates_with_uni_selection(self):

        user = LunaUsers.objects.filter(first_name='Roman').first()
        uni = Universities.objects.filter(name='KPI').first()


        data = {}
        data['uni_selection'] = []
        data['uni_selection'].append({
            'uni_id': f'{uni.id}',
            'user': f'{user.id}'
        })

        data_json = json.dumps(data)

        self.client.post(reverse('university_selected'), data=data_json, content_type='application/json')
        self.assertEqual(LunaUsers.objects.filter(first_name='Roman').first().uni, uni)

    # the user sees the email form on the front end with the university domain automatically there
    # the registration api sends the university domain extension to the front end

    def test_initialize_university_email_input(self):

        uni = Universities.objects.filter(name='KPI').first()

        data = {}
        data['email_domain_query'] = []
        data['email_domain_query'].append({
            'uni_id': f'{uni.id}'
        })

        json_data = json.dumps(data)

        response = self.client.post(reverse('uni_domain'), data=json_data, content_type='application/json')

        self.assertIn(f'{uni.domain}', str(response.content, encoding='utf8'))

    # the user fills in their email and sends it to the backend
    # when the email is sent to /register/{LunaUser_pk}/3 the user model is updated
    def test_user_inputs_email(self):
        user = LunaUsers.objects.filter(first_name='Roman').first()
        data = {}
        data['email'] = []
        data['email'].append({
            'email': 'roman@uni.com',
            'LunaUser': f'{user.id}'
            })
        data_json = json.dumps(data)

        response = self.client.post(reverse('email_input'), data=data_json, content_type='application/json')

        self.assertEqual(user.email, 'roman@uni.com')
        self.assertNotEqual(user.verification_key, 'Not yet sent') # make 'Not yet sent' the default value in the table

    # the user clicks the verification link and the user is verified
    # when the user navigates to /register/{LunaUser_pk}/verification/{secret_key}/ the LunaUser model is updated to say they are verified
    def test_user_email_verification(self):
        user = LunaUsers.objects.filter(first_name='Roman').first()

        response = self.client.get(reverse('validate_email'), kwargs={'LunaUser_id': f'{user.id}', 'secret_key': f'{user.verification_key}'})

        self.assertEqual(LunaUsers.objects.filter(first_name='Roman').first().verification_key, 'verified')
