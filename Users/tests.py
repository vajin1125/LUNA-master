from django.test import TestCase
from django.urls import reverse

from Uni_Socs.models import Universities_Societies, Universities
from Users.models import LunaUsers

import json


class User_updates_uni_societies(TestCase):

    def setUp(self):
        LunaUsers.objects.create(first_name='Roman', last_name='Synovets', fb_id='736587236532735', security_key='password')

        uni_kpi = Universities.objects.create(name='KPI')
        uni_oxford = Universities.objects.create(name='Oxford')

        Universities_Societies.objects.create(name='club_kpi_1', uni_fk=uni_kpi)
        Universities_Societies.objects.create(name='club_kpi_2', uni_fk=uni_kpi)
        Universities_Societies.objects.create(name='club_kpi_3', uni_fk=uni_kpi)
        Universities_Societies.objects.create(name='club_kpi_4', uni_fk=uni_kpi)

    def test_user_selects_uni_socs_to_follow(self):
        user = LunaUsers.objects.filter(first_name='Roman').first()
        soc1 = Universities_Societies.objects.filter(name='club_kpi_1').first()
        soc2 = Universities_Societies.objects.filter(name='club_kpi_2').first()
        soc3 = Universities_Societies.objects.filter(name='club_kpi_3').first()

        data = {}
        data['user'] = []
        data['user'].append({
            'user_id': f'{user.pk}'
        })
        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })
        data['uni_socs_selection'] = []
        data['uni_socs_selection'].append({
            'soc1': f'{soc1.id}',
            'soc2': f'{soc2.id}',
            'soc3': f'{soc3.id}',
            'soc4': None,
            'soc5': None,
            'soc6': None,
            'soc7': None,
            'soc8': None,
            'soc9': None,
            'soc10': None,
        })
        json_data = json.dumps(data)

        self.client.post(reverse('update_uni_following'), data=json_data, content_type='application/json')

        self.assertEquals(LunaUsers.objects.filter(first_name='Roman').first().soc1, soc1)
        self.assertEquals(LunaUsers.objects.filter(first_name='Roman').first().soc2, soc2)
        self.assertEquals(LunaUsers.objects.filter(first_name='Roman').first().soc3, soc3)

    def test_add_one_society_follow_on(self):

        user = LunaUsers.objects.filter(first_name='Roman').first()
        soc1 = Universities_Societies.objects.filter(name='club_kpi_1').first()
        soc2 = Universities_Societies.objects.filter(name='club_kpi_2').first()

        user.soc1_id = soc1
        user.soc2_id = soc2
        user.save()

        soc3 = Universities_Societies.objects.filter(name='club_kpi_3').first()

        data = {}
        data['user_security_key'] = []
        data['user_security_key'].append({
            'key':f'{user.security_key}'
            })
        
        data['user'] = []
        data['user'].append({
            'user_id': f'{user.id}'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        data['uni_socs_selection'] = []
        data['uni_socs_selection'].append({
            'soc_id': f'{soc3.id}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('toggle_uni_soc_following'), data=json_data, content_type='application/json')

        self.assertEquals(LunaUsers.objects.filter(first_name='Roman').first().soc3, soc3)

    def test_remove_one_society_follow_off(self):

        user = LunaUsers.objects.filter(first_name='Roman').first()
        soc1 = Universities_Societies.objects.filter(name='club_kpi_1').first()
        soc2 = Universities_Societies.objects.filter(name='club_kpi_2').first()

        user.soc1_id = soc1
        user.soc2_id = soc2
        user.save()

        data = {}
        data['user'] = []
        data['user'].append({
            'user_id': f'{user.id}'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        data['uni_socs_selection'] = []
        data['uni_socs_selection'].append({
            'soc_id': f'{soc2.id}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('toggle_uni_soc_unfollowing'), data=json_data, content_type='application/json')

        self.assertEquals(LunaUsers.objects.filter(first_name='Roman').first().soc2, None)

    def test_overflow_all_society_follow(self):
        uni_kpi_id = Universities.objects.filter(name='KPI').first()
        user = LunaUsers.objects.filter(first_name='Roman').first()

        soc1 = Universities_Societies.objects.filter(name='club_kpi_1').first()
        soc2 = Universities_Societies.objects.filter(name='club_kpi_2').first()
        soc3 = Universities_Societies.objects.filter(name='club_kpi_3').first()
        soc4 = Universities_Societies.objects.filter(name='club_kpi_4').first()

        soc5 = Universities_Societies.objects.create(name='club_kpi_5', uni_fk=uni_kpi_id)
        soc6 = Universities_Societies.objects.create(name='club_kpi_6', uni_fk=uni_kpi_id)
        soc7 = Universities_Societies.objects.create(name='club_kpi_7', uni_fk=uni_kpi_id)

        soc8 = Universities_Societies.objects.create(name='club_kpi_8', uni_fk=uni_kpi_id)
        soc9 = Universities_Societies.objects.create(name='club_kpi_9', uni_fk=uni_kpi_id)
        soc10 = Universities_Societies.objects.create(name='club_kpi_10', uni_fk=uni_kpi_id)

        soc11 = Universities_Societies.objects.create(name='club_kpi_11', uni_fk=uni_kpi_id)

        user.soc1_id = soc1
        user.soc2_id = soc2
        user.soc3_id = soc3
        user.soc4_id = soc4

        user.soc5_id = soc5
        user.soc6_id = soc6
        user.soc7_id = soc7
        user.soc8_id = soc8

        user.soc9_id = soc9
        user.soc10_id = soc10

        user.save()

        data = {}
        data['user'] = []
        data['user'].append({
            'user_id': f'{user.id}'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        data['uni_socs_selection'] = []
        data['uni_socs_selection'].append({
            'soc_id': f'{soc11.id}'
        })

        json_data = json.dumps(data)

        response = self.client.post(reverse('toggle_uni_soc_following'), data=json_data, content_type='application/json', encoding='utf8')
        json_data = json.loads(response.content)

        self.assertEqual(json_data['response'][0]['get_response'], 'reached society following limit')


class TestUserProfile(TestCase):
    def setUp(self):
        uni_kpi = Universities.objects.create(name='KPI')

        soc1_id = Universities_Societies.objects.create(name='club_kpi_1', uni_fk=uni_kpi)
        soc2_id = Universities_Societies.objects.create(name='club_kpi_2', uni_fk=uni_kpi)
        soc3_id = Universities_Societies.objects.create(name='club_kpi_3', uni_fk=uni_kpi)
        soc4_id = Universities_Societies.objects.create(name='club_kpi_4', uni_fk=uni_kpi)

        LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='736587236532735', security_key='RomanIsABadassRoman', soc1_id=soc1_id.id,
                                 soc2_id=soc2_id.id, soc3_id=soc3_id.id)

    def test_profile_user(self):
        user = LunaUsers.objects.filter(fb_id='736587236532735').first()
        uni_kpi = Universities.objects.filter(name='KPI').first()

        soc1_id = Universities_Societies.objects.filter(name='club_kpi_1', uni_fk=uni_kpi).first()
        soc2_id = Universities_Societies.objects.filter(name='club_kpi_2', uni_fk=uni_kpi).first()
        soc3_id = Universities_Societies.objects.filter(name='club_kpi_3', uni_fk=uni_kpi).first()

        uni_soc_not_followed = Universities_Societies.objects.filter(name='club_kpi_4', uni_fk=uni_kpi.id).first()

        data = {}
        data['user_profile_request'] = []
        data['user_profile_request'].append({
            'user_id': user.id
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })
        
        json_data = json.dumps(data)

        response = self.client.post(reverse('user_profile'), data=json_data, content_type='application/json', encoding='utf8')
        json_data = json.loads(response.content)

        self.assertEqual(json_data['followed_user_uni_soc'][0]['uni_soc_id'], soc1_id.id)
        self.assertEqual(json_data['followed_user_uni_soc'][0]['uni_soc_name'], soc1_id.name)
        self.assertEqual(json_data['followed_user_uni_soc'][0]['uni_soc_cover_photo'], soc1_id.cover_photo)

        self.assertEqual(json_data['followed_user_uni_soc'][1]['uni_soc_id'], soc2_id.id)
        self.assertEqual(json_data['followed_user_uni_soc'][1]['uni_soc_name'], soc2_id.name)
        self.assertEqual(json_data['followed_user_uni_soc'][1]['uni_soc_cover_photo'], soc2_id.cover_photo)

        self.assertEqual(json_data['followed_user_uni_soc'][2]['uni_soc_id'], soc3_id.id)
        self.assertEqual(json_data['followed_user_uni_soc'][2]['uni_soc_name'], soc3_id.name)
        self.assertEqual(json_data['followed_user_uni_soc'][2]['uni_soc_cover_photo'], soc3_id.cover_photo)

        self.assertNotIn(str(response.content, encoding='utf8'), str(uni_soc_not_followed.id))
