from django.test import TestCase
from django.urls import reverse

import datetime
import json

from Users.models import LunaUsers, RSVP_event
from Uni_Socs.models import Universities, Universities_Societies, Events

from LUNA_API.settings import LOREM_IPSUM


# HELP METHOD
def convert_to_date(str_date, form='%Y-%m-%d'):
    dt = datetime.datetime.strptime(str_date, form)
    return dt.date()


def convert_to_time(str_time, form='%H:%M:%S'):
    dt = datetime.datetime.strptime(str_time, form)
    return dt.time()
# ###########


class TestFeed(TestCase):

    def setUp(self):
        uni_zifer = Universities.objects.create(name='ziferblat', domain='@ziferblat.com', uni_facebook_id='ziferblat')
        uni_kpi = Universities.objects.create(name='KPI', domain='@kpi.com', uni_facebook_id='kpi.ua')

        uni_socs_zifer_kiev = Universities_Societies.objects.create(name='ziferblat_kiev', uni_fk=uni_zifer, fb_id='ClockfaceKiev')
        uni_socs_zifer_london = Universities_Societies.objects.create(name='ziferblat_london', uni_fk=uni_zifer, fb_id='ZiferblatLondon')

        uni_socs_kpi_live = Universities_Societies.objects.create(name='kpi_live', uni_fk=uni_kpi, fb_id='kpi.live.ua')
        uni_socs_kpi_new = Universities_Societies.objects.create(name='kpi_new', uni_fk=uni_zifer, fb_id='kpi.new.ua')

        Events.objects.create(
            cover_photo='URL Photo',
            title='Open Day', date='2019-10-25', time='14:30:59', address='Lomonosova street 22',
            tickets=True, description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='URL Photo',
            title='Master Class', date='2018-06-25', time='15:00:00', address='Khreschatik street 7',
            tickets=True, description=LOREM_IPSUM, uni_socs=uni_socs_zifer_london)

        Events.objects.create(
            cover_photo='URL Photo',
            title='HALLOWEEN', date='2018-10-31', time='18:30:00', address='Kosak street 11/2',
            tickets=True, description=LOREM_IPSUM, uni_socs=uni_socs_kpi_new)

        LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='100025605049892', security_key='Romanisabadassroman', uni_id=uni_zifer.id,
                                 soc1_id=uni_socs_zifer_kiev.id, soc2_id=uni_socs_zifer_london.id)

        LunaUsers.objects.create(first_name='Alex', last_name='Beskine',
                                 fb_id='325748564378578', security_key='Romanisabadassroman', uni_id=uni_kpi.id,
                                 soc1_id=uni_socs_kpi_live.id, soc2_id=uni_socs_kpi_new.id)

    def test_feed_request(self):
        # request json for feed/user_id
        # the phone sends a json request to the django api requesting the 'feed' for a user
        # http response returns all events from all clubs the user is subscribed to in chronological order

        user = LunaUsers.objects.filter(first_name='Roman').first()

        eventOne = Events.objects.filter(date='2019-10-25').first()
        eventTwo = Events.objects.filter(date='2018-06-25').first()
        eventThree = Events.objects.filter(date='2018-10-31').first()

        data = {}
        data['request_homepage_events_feed'] = []
        data['request_homepage_events_feed'].append({
            'user_id': user.id
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        response = self.client.post(reverse('feed'), data=json_data, content_type='application/json', encoding='utf8')

        # 2. to check the response.
        json_data = json.loads(response.content)

        self.assertEquals(convert_to_date(json_data['event'][0]['date']), eventTwo.date)
        self.assertEquals(convert_to_date(json_data['event'][1]['date']), eventOne.date)

        self.assertNotEquals(json_data['event'][0]['date'], eventThree.date)


class TestEventPage(TestCase):

    def setUp(self):

        uni_zifer = Universities.objects.create(name='ziferblat', domain='@ziferblat.com', uni_facebook_id='ziferblat')
        uni_kpi = Universities.objects.create(name='KPI', domain='@kpi.com', uni_facebook_id='kpi.ua')

        uni_socs_zifer_kiev = Universities_Societies.objects.create(name='ziferblat_kiev',
                                                                    uni_fk=uni_zifer, fb_id='ClockfaceKiev')

        uni_socs_zifer_london = Universities_Societies.objects.create(name='ziferblat_london',
                                                                      uni_fk=uni_zifer, fb_id='ZiferblatLondon')

        uni_socs_kpi_live = Universities_Societies.objects.create(name='kpi_live',
                                                                  uni_fk=uni_kpi, fb_id='kpi.live.ua')

        uni_socs_kpi_new = Universities_Societies.objects.create(name='kpi_new',
                                                                 uni_fk=uni_zifer, fb_id='kpi.new.ua')

        event_Roman = Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/17951589_1530049737029338_6097412397112960843_n.jpg?_nc_cat=0&oh=0cc46e845b79620df1dc8c48f983aea3&oe=5B9C4415',
            title='Open Day', date='2019-10-25', time='14:30:59', address='Lomonosova street 22',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class', date='2018-06-25', time='15:00:00', address='Khreschatik street 7',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_london)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/12191829_1024805910896755_1695393036035372599_n.jpg?_nc_cat=0&oh=87e43900078707f93c308a494aea50aa&oe=5B4F362E',
            title='HALLOWEEN', date='2018-10-31', time='18:30:00', address='Kosak street 11/2',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_kpi_new)


        user_Roman = LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                              fb_id='100025605049892', security_key='Romanisabadassroman', uni_id=uni_zifer.id,
                                              soc1_id=uni_socs_zifer_kiev.id, soc2_id=uni_socs_zifer_london.id)

        LunaUsers.objects.create(first_name='Alex', last_name='Beskine',
                                 fb_id='325748564378578', security_key='Romanisabadassroman', uni_id=uni_kpi.id,
                                 soc1_id=uni_socs_kpi_live.id, soc2_id=uni_socs_kpi_new.id)


        RSVP_event.objects.create(user=user_Roman, event=event_Roman)

    def test_view_event_page_request(self):
        # the user has clicked an event
        # the phone needs to load all the details of the event on a seperate page
        # the phone sends a signal to the django api requesting all the details of that event:
        # the event id
        # the lunauser id

        # assert the api sends back to the phone:
        # the event title
        # the event description
        # time
        # date
        # address
        # event_cover_photo
        # club_profile_photo
        # tickets_information
        # the event_id
        # the club_id
        # the user's RSVP status to this event (он уже собирается на это мероприятие? да, нет, интересно?)
        # <-- Roman, this is where you will need to use the RSVP_events_model

        user = LunaUsers.objects.filter(first_name='Roman').first()
        event = Events.objects.filter(date='2019-10-25').first()

        data = {}
        data['event_page_request'] = []
        data['event_page_request'].append({
            'user_id': user.id,
            'event_id': event.id,
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        response = self.client.post(reverse('event_detail'), data=json_data, content_type='application/json',
                                    encoding='utf8')

        # 2. to check the response.
        json_data = json.loads(response.content)

        self.assertEqual(json_data['event'][0]['title'], event.title)
        self.assertEqual(convert_to_date(json_data['event'][0]['date']), event.date)
        self.assertEqual(json_data['event'][0]['description'], event.description)
        self.assertEqual(convert_to_time(json_data['event'][0]['time']), event.time)
        self.assertEqual(json_data['event'][0]['address'], event.address)
        self.assertEqual(json_data['event'][0]['tickets'], event.tickets)
        self.assertEqual(json_data['event'][0]['event_cover_photo'], event.cover_photo)
        self.assertEqual(json_data['event'][0]['club_cover_photo'], event.uni_socs.cover_photo)
        self.assertEqual(json_data['event'][0]['tickets'], event.tickets)
        self.assertEqual(json_data['event'][0]['event_id'], event.id)
        self.assertEqual(json_data['event'][0]['club_id'], event.uni_socs.id)
        self.assertEqual(json_data['event'][0]['status'],
                         RSVP_event.objects.filter(user=user.id, event=event.id).first().status)

    def test_send_RSVP_YES(self):  # когда пользователь выбирает, идти ли на мероприятие или нет, или если он просто заинтересован.  Здесь мы тестируем, что база данных будет правильно обновляться
        # the user has decided to attend an event
        # he presses on the phone the button to 'attend'
        # the phone tells the django api that this user has decided to attend this event
        # the phone sends a json signal to the api containing:
        # the user id
        # the event id
        # the the user's RSVP response <-- Roman, Этот ответ будет да, нет или «заинтересован» - этот тест тестирует «да». «нет» и «заинтересованы» в двух отдельных тестах ниже.


        # assert the database has updated to have an object in the 'RSVP_event' table: <-- Roman, this could be a NEW object (if this is the first time the user is interacting with the event) or a PRE-EXISTING object (if the user is changing his mind on a decision previously made)
        # user = the current lunauser
        # event = foreignkey to the event
        # status = 'YES'
        user = LunaUsers.objects.filter(first_name='Roman').first()
        event = Events.objects.filter(date='2019-10-25').first()

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'YES'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        new_RSVP_object = RSVP_event.objects.filter(user=user.id, event=event.id).first()

        self.assertEqual(data['send_RSVP'][0]['user_id'], new_RSVP_object.user.id)
        self.assertEqual(data['send_RSVP'][0]['event_id'], new_RSVP_object.event.id)
        self.assertEqual(data['send_RSVP'][0]['RSVP_event_status'], new_RSVP_object.status)

    def test_send_RSVP_NO(self):  # когда пользователь выбирает, идти ли на мероприятие или нет, или если он просто заинтересован.  Здесь мы тестируем, что база данных будет правильно обновляться
        # the user has decided to attend an event
        # he presses on the phone the button to 'attend'
        # the phone tells the django api that this user has decided to attend this event
        # the phone sends a json signal to the api containing:
        # the user id
        # the event id
        # the the user's RSVP response

        # assert the database has updated to have an object in the 'RSVP_event' table: <-- Roman, this could be a NEW object (if this is the first time the user is interacting with the event) or a PRE-EXISTING object (if the user is changing his mind on a decision previously made)
        # user = the current lunauser
        # event = foreignkey to the event
        # status = 'NO'

        user = LunaUsers.objects.filter(first_name='Roman').first()
        event = Events.objects.filter(date='2019-10-25').first()

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'NO'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        new_RSVP_object = RSVP_event.objects.filter(user=user.id, event=event.id).first()

        self.assertEqual(data['send_RSVP'][0]['user_id'], new_RSVP_object.user.id)
        self.assertEqual(data['send_RSVP'][0]['event_id'], new_RSVP_object.event.id)
        self.assertEqual(data['send_RSVP'][0]['RSVP_event_status'], new_RSVP_object.status)

    def test_send_RSVP_INTERESTED(self):  # когда пользователь выбирает, идти ли на мероприятие или нет, или если он просто заинтересован.  Здесь мы тестируем, что база данных будет правильно обновляться
        # the user has decided to attend an event
        # he presses on the phone the button to 'attend'
        # the phone tells the django api that this user has decided to attend this event
        # the phone sends a json signal to the api containing:
        # the user id
        # the event id
        # the the user's RSVP response

        # assert the database has updated to have an object in the 'RSVP_event' table: <-- Roman, this could be a NEW object (if this is the first time the user is interacting with the event) or a PRE-EXISTING object (if the user is changing his mind on a decision previously made)
        # user = the current lunauser
        # event = foreignkey to the event
        # status = 'INTERESTED'

        user = LunaUsers.objects.filter(first_name='Roman').first()
        event = Events.objects.filter(date='2019-10-25').first()

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'INTERESTED'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        new_RSVP_object = RSVP_event.objects.filter(user=user, event=event).first()

        self.assertEqual(data['send_RSVP'][0]['user_id'], new_RSVP_object.user.id)
        self.assertEqual(data['send_RSVP'][0]['event_id'], new_RSVP_object.event.id)
        self.assertEqual(data['send_RSVP'][0]['RSVP_event_status'], new_RSVP_object.status)

    def test_new_object_not_created_when_user_changing_RSVP(self):  # 1. пользователь решает перейти к событию. 2. объект создается в таблице событий RSVP. 3. пользователь меняет свое решение ==== нам нужно убедиться, что один и тот же объект обновлен, а не новый созданный объект.
        # the user RSVP YES to go to an event he has not previously interacted with 
        # assert a new object is created in the database

        # the user changes his mind and RSVP NO to the same event
        # assert that the same object as above is updated, not a new object created#

        user = LunaUsers.objects.filter(first_name='Roman').first()
        event = Events.objects.filter(date='2019-10-25').first()

        # 1. the user RSVP YES the event

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'YES'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        original_RSVP_object = RSVP_event.objects.filter(user=user, event=event).first()
        self.assertEquals(original_RSVP_object.status, 'YES')

        # 2. the user changes his mind and says 'NO' to the event

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'NO'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        # we check that it is the original rsvp object that has changed and no new one has been made
        unchanged_RSVP_object = RSVP_event.objects.filter(user=user, event=event).first()

        self.assertEquals(RSVP_event.objects.filter(user=user, event=event).count(), 1)
        self.assertEquals(unchanged_RSVP_object.status, 'NO')

        # 3. the user changes his mind again and says 'INTERESTED' to the event

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'INTERESTED'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        # we check that it is the original rsvp object that has chanced and no new one has been made

        original_RSVP_object = RSVP_event.objects.filter(user=user, event=event).first()
        self.assertEquals(original_RSVP_object.status, 'INTERESTED')
        self.assertEquals(RSVP_event.objects.filter(user=user, event=event).count(), 1)

        # 4. the user changes his mind again and says 'YES' afterall to the event

        data = {}
        data['send_RSVP'] = []
        data['send_RSVP'].append({
            'user_id': user.id,
            'event_id': event.id,
            'RSVP_event_status': 'YES'
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        self.client.post(reverse('rsvp_status_change'), data=json_data, content_type='application/json',
                         encoding='utf8')

        original_RSVP_object = RSVP_event.objects.filter(user=user, event=event).first()

        self.assertEquals(original_RSVP_object.status, 'YES')
        self.assertEquals(RSVP_event.objects.filter(user=user, event=event).count(), 1)


class TestUniSocProfile(TestCase):
    def setUp(self):
        # universities
        uni_zifer = Universities.objects.create(
            name='ziferblat',
            domain='@ziferblat.com',
            uni_facebook_id='ziferblat'
            )
        # university_societies
        uni_socs_zifer_kiev = Universities_Societies.objects.create(
            name='ziferblat_kiev',
            uni_fk=uni_zifer,
            fb_id='ClockfaceKiev'
            )
        uni_socs_other = Universities_Societies.objects.create(
            name='other',
            uni_fk=uni_zifer,
            fb_id='ClockfaceKiev'
        )

        # make six Events in order to test that only five are sent back
        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/17951589_1530049737029338_6097412397112960843_n.jpg?_nc_cat=0&oh=0cc46e845b79620df1dc8c48f983aea3&oe=5B9C4415',
            title='Master Class 1', date='2018-10-25', time='14:30:59', address='Lomonosova street 22',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class 2', date='2019-06-25', time='15:00:00', address='Khreschatik street 7',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class 3', date='2020-06-25', time='15:00:00', address='Khreschatik street 8',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class 4', date='2021-06-25', time='15:00:00', address='Khreschatik street 9',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class 5', date='2022-06-25', time='15:00:00', address='Khreschatik street 9',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

            # this one will not be sent back to the uni_soc_profile_page
        Events.objects.create(
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18952747_1503343539709654_7407432562906946592_n.jpg?_nc_cat=0&oh=5b38e280aa040ff312d8708f07274bd8&oe=5B9C9504',
            title='Master Class 6', date='2023-06-25', time='15:00:00', address='Khreschatik street 10',
            tickets='tickets needed - buy here: www.google.com', description=LOREM_IPSUM, uni_socs=uni_socs_zifer_kiev)

        # Luna User
        LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='100025605049892', security_key='RomanIsABadassRoman', uni_id=uni_zifer.id,
                                 soc1_id=uni_socs_zifer_kiev.id)

    def test_loading_uni_soc_profile_page_all_correct_information(self):

        followed_uni_soc = Universities_Societies.objects.filter(name='ziferblat_kiev').first()
        user = LunaUsers.objects.filter(first_name='Roman', soc1_id=followed_uni_soc.id).first()
        not_followed_uni_soc = Universities_Societies.objects.filter(name='other').first()

        uni_soc_profile_page_events = []

        uni_soc_profile_page_events.append(Events.objects.filter(title='Master Class 1').first())
        uni_soc_profile_page_events.append(Events.objects.filter(title='Master Class 2').first())
        uni_soc_profile_page_events.append(Events.objects.filter(title='Master Class 3').first())
        uni_soc_profile_page_events.append(Events.objects.filter(title='Master Class 4').first())
        uni_soc_profile_page_events.append(Events.objects.filter(title='Master Class 5').first())

        data = {}
        data['uni_soc_profile_page_request'] = []
        data['uni_soc_profile_page_request'].append({
            'user_id': user.id,
            'uni_socs_id': followed_uni_soc.id,
        })

        data['user_id'] = []
        data['user_id'].append({
            'user_id': user.id,
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        response = self.client.post(reverse('profile'), data=json_data, content_type='application/json', encoding='utf8')

        json_data = json.loads(response.content)

        # test all correct info sent back

        self.assertEqual(json_data['uni_soc_profile'][0]['name'], followed_uni_soc.name)
        self.assertEqual(json_data['uni_soc_profile'][0]['cover_photo'], followed_uni_soc.cover_photo)
        self.assertEqual(json_data['uni_soc_profile'][0]['about'], followed_uni_soc.about)
        self.assertEqual(json_data['uni_soc_profile'][0]['web_site'], followed_uni_soc.web_site)
        self.assertEqual(json_data['uni_soc_profile'][0]['phone'], followed_uni_soc.phone)
        self.assertEqual(json_data['uni_soc_profile'][0]['address'], followed_uni_soc.address)
        self.assertEqual(json_data['uni_soc_profile'][0]['user_follow_status'], 'True')

        # assert event list sent
        a = 0
        for i in uni_soc_profile_page_events:
            self.assertEqual(json_data['uni_soc_events'][a]['title'], i.title)
            self.assertEqual(convert_to_date(json_data['uni_soc_events'][a]['date']), i.date)
            self.assertEqual(json_data['uni_soc_events'][a]['cover_photo'], i.cover_photo)
            self.assertEqual(json_data['uni_soc_events'][a]['id'], i.id)
            a += 1

        # assert that the event list is only five
        self.assertEqual(len(json_data['uni_soc_events']), 5)

        # assert it is sent in chronological order

    def test_loading_uni_soc_profile_not_followed_returns_not_followed_info(self):
        not_followed_uni_soc = Universities_Societies.objects.filter(name='other').first()
        user = LunaUsers.objects.filter(first_name='Roman').first()

        data = {}
        data['uni_soc_profile_page_request'] = []
        data['uni_soc_profile_page_request'].append({
            'user_id': user.id,
            'uni_socs_id': not_followed_uni_soc.id,
        })

        data['user_id'] = []
        data['user_id'].append({
            'user_id': user.id,
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        response = self.client.post(reverse('profile'), data=json_data, content_type='application/json', encoding='utf8')

        json_data = json.loads(response.content)

        self.assertEqual(json_data['uni_soc_profile'][0]['user_follow_status'], 'False')

    def test_loading_uni_soc_profile_all_events(self):

        user = LunaUsers.objects.filter(first_name='Roman').first()
        uni_soc_id = Universities_Societies.objects.filter(name='ziferblat_kiev').first()
        uni_soc_all_events = Events.objects.filter(uni_socs=uni_soc_id)

        data={}
        data['uni_soc_all_events_page_request'] = []
        data['uni_soc_all_events_page_request'].append({
            'uni_soc_id':uni_soc_id.id
            })

        data['user_id'] = []
        data['user_id'].append({
            'user_id': user.id,
        })
        
        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)
        response = self.client.post(reverse('uni_soc_profile_all_events'), data=json_data, content_type='application/json', encoding='utf8')

        json_data = json.loads(response.content)

        a = 0
        for i in uni_soc_all_events:
            self.assertEqual(json_data['uni_soc_all_events'][a]['title'], i.title)
            self.assertEqual(json_data['uni_soc_all_events'][a]['cover_photo'], i.cover_photo)
            self.assertEqual(convert_to_date(json_data['uni_soc_all_events'][a]['date']), i.date)
            a += 1


class TestSearch(TestCase):
    def setUp(self):
        uni_kpi = Universities.objects.create(name='KPI')
        oxford = Universities.objects.create(name='Oxford')

        # KPI uni_socs
        kpi_club_1 = Universities_Societies.objects.create(name='club_kpi_1', uni_fk=uni_kpi)
        kpi_club_2 = Universities_Societies.objects.create(name='club_kpi_2', uni_fk=uni_kpi)
        kpi_club_3 = Universities_Societies.objects.create(name='club_kpi_3', uni_fk=uni_kpi)

        # Oxford uni_socs
        club_oxford_1 = Universities_Societies.objects.create(name='club_oxford_1', uni_fk=oxford)
        Universities_Societies.objects.create(name='club_oxford_2', uni_fk=oxford)

        # Luna Users
        LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='736587236532735', security_key='RomanIsABadassRoman', uni=uni_kpi)

        LunaUsers.objects.create(first_name='Alex', last_name='Beskine',
                                 fb_id='845643865728763', security_key='RomanIsABadassRoman', uni=oxford)
        # Events
        Events.objects.create(
            cover_photo='Photo URL', title='Master Class', date='2018-06-25',
            time='15:00:00', address='Khreschatik street 7',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_1)

        Events.objects.create(
            cover_photo='Photo URL', title='Some Title', date='2018-07-03',
            time='15:20:00', address='Lol street 55',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_1)

        Events.objects.create(
            cover_photo='Photo URL', title='Orchestre', date='2018-11-11',
            time='19:45:00', address='Lorem street 14',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_2)

        Events.objects.create(
            cover_photo='Photo URL', title='HALLOWEEN', date='2018-10-31',
            time='18:30:00', address='Kosak street 11/2',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_2)

        Events.objects.create(
            cover_photo='Photo URL', title='4 July', date='2018-06-04',
            time='18:30:00', address='Green street 455',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_3)

        Events.objects.create(
            cover_photo='Photo URL', title='4 July', date='2018-03-04',
            time='18:30:00', address='Green street 455',
            tickets=True, description=LOREM_IPSUM, uni_socs=club_oxford_1)

    def test_search_all_event_from_followed_university(self):
        # setup user for KPI university
        user = LunaUsers.objects.filter(fb_id='736587236532735').first()

        # get all from (uni socs kpi)
        all_uni_socs_kpi = Universities_Societies.objects.filter(uni_fk=user.uni).all()

        merged_unsorted_queryset = Events.objects.none()

        for soc in all_uni_socs_kpi:
            merged_unsorted_queryset = merged_unsorted_queryset.union(Events.objects.filter(uni_socs=soc.id))

        # get sorted queryset from Events model
        sorted_by_date_queryset = merged_unsorted_queryset.order_by('date')

        # send all_events_search request to server as json containing the user id
        data = {}
        data['user_all_uni_events_request'] = []
        data['user_all_uni_events_request'].append({
            'user_id': user.id,
            'date_range_1': None,
            'date_range_2': None,
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)

        response = self.client.post(reverse('search_all_events'), data=json_data, content_type='application/json',
                                    encoding='utf8')
        data = json.loads(response.content)

        # make sure that all the correct events are present, in chronological order
        a = 0
        for i in sorted_by_date_queryset:
            self.assertEqual(convert_to_date(data['all_from_uni_event'][a]['date']), i.date)
            self.assertEqual(data['all_from_uni_event'][a]['id'], i.id)
            a += 1

    def test_search_advanced_event_from_followed_university(self):
        # setup user for KPI university
        user = LunaUsers.objects.filter(fb_id='736587236532735').first()

        # we receive all events from the date 2018-06-04 through 2018-11-10
        event_1 = Events.objects.filter(date='2018-06-04').first()
        event_2 = Events.objects.filter(date='2018-06-25').first()
        event_3 = Events.objects.filter(date='2018-07-03').first()
        event_4 = Events.objects.filter(date='2018-10-31').first()
        event_5 = Events.objects.filter(date='2018-11-11').first()

        # get all from (uni socs kpi)
        all_uni_socs_kpi = Universities_Societies.objects.filter(uni_fk=user.uni).all()

        # send all_events_search request to server as json containing the user id
        data = {}
        data['user_all_uni_events_request'] = []
        data['user_all_uni_events_request'].append({
            'user_id': user.id,
            'date_range_1': '2018-06-03',
            'date_range_2': '2018-11-10',
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })

        json_data = json.dumps(data)

        response = self.client.post(reverse('search_all_events'), data=json_data, content_type='application/json',
                                    encoding='utf8')
        data = json.loads(response.content)

        self.assertEqual(convert_to_date(data['all_from_uni_event'][0]['date']), event_1.date)
        self.assertEqual(convert_to_date(data['all_from_uni_event'][1]['date']), event_2.date)
        self.assertEqual(convert_to_date(data['all_from_uni_event'][2]['date']), event_3.date)
        self.assertNotEquals(convert_to_date(data['all_from_uni_event'][3]['date']), event_5.date)


class TestMyEvents(TestCase):
    def setUp(self):
        uni_kpi = Universities.objects.create(name='KPI')

        # KPI uni_socs
        kpi_club_1 = Universities_Societies.objects.create(name='club_kpi_1', uni_fk=uni_kpi)
        kpi_club_2 = Universities_Societies.objects.create(name='club_kpi_2', uni_fk=uni_kpi)
        kpi_club_3 = Universities_Societies.objects.create(name='club_kpi_3', uni_fk=uni_kpi)

        # Luna Users
        user = LunaUsers.objects.create(first_name='Roman', last_name='Synovets',
                                 fb_id='736587236532735', security_key='RomanIsABadassRoman', uni=uni_kpi)

        # Events
        event_1 = Events.objects.create(
            cover_photo='Photo URL', title='Master Class', date='2018-06-25',
            time='15:00:00', address='Khreschatik street 7',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_1)

        event_2 = Events.objects.create(
            cover_photo='Photo URL', title='Some Title', date='2018-07-03',
            time='15:20:00', address='Lol street 55',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_1)

        event_3 = Events.objects.create(
            cover_photo='Photo URL', title='Orchestre', date='2018-11-11',
            time='19:45:00', address='Lorem street 14',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_2)

        event_4 = Events.objects.create(
            cover_photo='Photo URL', title='HALLOWEEN', date='2018-10-31',
            time='18:30:00', address='Kosak street 11/2',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_2)

        event_5 = Events.objects.create(
            cover_photo='Photo URL', title='4 July', date='2018-06-04',
            time='18:30:00', address='Green street 455',
            tickets=True, description=LOREM_IPSUM, uni_socs=kpi_club_3)

        RSVP_event.objects.create(user=user, event=event_1, status='YES')
        RSVP_event.objects.create(user=user, event=event_2, status='YES')
        RSVP_event.objects.create(user=user, event=event_3, status='YES')
        RSVP_event.objects.create(user=user, event=event_4, status='YES')
        RSVP_event.objects.create(user=user, event=event_5, status='NO')

    def test_my_events_request(self):
        # Get user
        user = LunaUsers.objects.filter(fb_id='736587236532735').first()

        # Retrieving all events in chronological order
        event_a = Events.objects.filter(date='2018-06-25').first()
        event_b = Events.objects.filter(date='2018-07-03').first()
        event_d = Events.objects.filter(date='2018-11-11').first() #
        event_c = Events.objects.filter(date='2018-10-31').first() #

        # user_RSVPs = RSVP_event.objects.filter(user=user.id, status='YES')

        # client request to the server to get a -
        # list of all its events for which it is signed
        data = {}
        data['request_for_my_events'] = []
        data['request_for_my_events'].append({
            'user_id': user.id
        })

        data['user_security_key'] = []
        data['user_security_key'].append({
            'key': f'{user.security_key}'
        })
        
        json_data = json.dumps(data)

        response = self.client.post(reverse('my_events'), data=json_data, content_type='application/json', encoding='utf8')
        json_data = json.loads(response.content)

        self.assertEqual(json_data['my_events'][0]['id'], event_a.id)
        self.assertEqual(json_data['my_events'][0]['cover_photo'], event_a.cover_photo)
        self.assertEqual(convert_to_date(json_data['my_events'][0]['date']), event_a.date)
        self.assertEqual(convert_to_time(json_data['my_events'][0]['time']), event_a.time)
        self.assertEqual(json_data['my_events'][0]['address'], event_a.address)

        self.assertEqual(json_data['my_events'][1]['id'], event_b.id)
        self.assertEqual(json_data['my_events'][1]['cover_photo'], event_b.cover_photo)
        self.assertEqual(convert_to_date(json_data['my_events'][1]['date']), event_b.date)
        self.assertEqual(convert_to_time(json_data['my_events'][1]['time']), event_b.time)
        self.assertEqual(json_data['my_events'][1]['address'], event_b.address)

        self.assertEqual(json_data['my_events'][2]['id'], event_c.id)
        self.assertEqual(json_data['my_events'][2]['cover_photo'], event_c.cover_photo)
        self.assertEqual(convert_to_date(json_data['my_events'][2]['date']), event_c.date)
        self.assertEqual(convert_to_time(json_data['my_events'][2]['time']), event_c.time)
        self.assertEqual(json_data['my_events'][2]['address'], event_c.address)

        self.assertEqual(json_data['my_events'][3]['id'], event_d.id)
        self.assertEqual(json_data['my_events'][3]['cover_photo'], event_d.cover_photo)
        self.assertEqual(convert_to_date(json_data['my_events'][3]['date']), event_d.date)
        self.assertEqual(convert_to_time(json_data['my_events'][3]['time']), event_d.time)
        self.assertEqual(json_data['my_events'][3]['address'], event_d.address)

