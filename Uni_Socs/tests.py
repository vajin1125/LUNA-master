from django.test import TestCase
from django.urls import reverse

from Uni_Socs.models import Universities_Societies, Universities
from Users.models import LunaUsers

import json


class Universities_Societies_query(TestCase):
    #
    #   SetUp for Test
    #
    def setUp(self):

        uni_kpi = Universities.objects.create(name='KPI')
        uni_oxford = Universities.objects.create(name='Oxford')

        club_kpi_1 = Universities_Societies.objects.create(name='club_kpi_1', uni_fk=uni_kpi)
        club_kpi_2 = Universities_Societies.objects.create(name='club_kpi_2', uni_fk=uni_kpi)
        club_kpi_3 = Universities_Societies.objects.create(name='club_kpi_3', uni_fk=uni_kpi)

        Universities_Societies.objects.create(name='club_oxford_1', uni_fk=uni_oxford)
        Universities_Societies.objects.create(name='club_oxford_2', uni_fk=uni_oxford)
        Universities_Societies.objects.create(name='club_oxford_3', uni_fk=uni_oxford)

        LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='736587236532735', security_key='RomanIsABadassRoman', soc1_id=club_kpi_1.id, soc2_id=club_kpi_2.id)

    #
    # when the user is verified the user selects which clubs to follow
    # when a user is following zero university societies -
    # the api sends to the front end all the available societies to follow
    #
    def test_request_all_uni_socs_info(self): # all available societies for the user to follow
        user = LunaUsers.objects.filter(fb_id='736587236532735').first()
        uni = Universities.objects.filter(name='KPI').first()

        data = {}
        data['uni_socs_query'] = []
        data['uni_socs_query'].append({
            'user_id': user.id,
            'uni_id': uni.id,
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)

        response = self.client.post(reverse('query_clubs'), data=json_data, content_type='application/json')
        get_uni_socs = Universities_Societies.objects.filter(uni_fk=uni)

        json_data = json.loads(response.content)
        iterator = 0

        for i in get_uni_socs:
            self.assertEqual(i.name, json_data['uni_socs'][iterator]['name'])
            self.assertEqual(i.id, json_data['uni_socs'][iterator]['id'])
            self.assertEqual(i.cover_photo, json_data['uni_socs'][iterator]['cover_photo'])
            iterator += 1

        self.assertEqual(json_data['uni_socs'][0]['follow'], 'NO')
        self.assertEqual(json_data['uni_socs'][1]['follow'], 'YES')
        self.assertEqual(json_data['uni_socs'][2]['follow'], 'YES')




