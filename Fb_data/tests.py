from django.test import TestCase
from django.urls import reverse

from Uni_Socs.models import Universities, Universities_Societies, Events
from Users.models import LunaUsers

import datetime


class Data_entry(TestCase):

    def setUp(self):
        Universities.objects.create(
            name='Ziferblat Worldwide',
            domain='@zf.com',
            uni_facebook_id='Ziferblat',
            description='Ziferblat is a growing chain of 14 spaces all over Russia, Ukraine, Great Britain and Slovenia.',
            cover_photo='https://scontent.fiev4-1.fna.fbcdn.net/v/t1.0-9/18118587_1399334340126599_6268802801859959663_n.png?_nc_cat=0&oh=a0e3aafd22f4b0029a3ce07694812c82&oe=5B996580',
        )

        Universities_Societies.objects.create(
            name='Ziferblat Kiev',
            uni_fk=Universities.objects.filter(name='Ziferblat Worldwide').first(),
            fb_id='ClockfaceKiev',
            description='Coffee Shop in Kyiv, Ukraine'
        )

    def test_add_new_university(self):
        # a form is filled in with the:
        new_uni_data = {
            'domain': '@ucl.com',
            'uni_facebook_id': 'uclofficial',
        }

        # the form data is posted to the 'new_university' function
        self.client.post(reverse('add_university'), data=new_uni_data)

        # the database is updated with the university and all it's corect information
        new_university_object = Universities.objects.filter(name='UCL').first()

        self.assertEquals(new_university_object.name, 'UCL')
        self.assertEquals(new_university_object.domain, '@ucl.com')
        self.assertEquals(new_university_object.uni_facebook_id, '92637159209')
        self.assertEquals(new_university_object.cover_photo,
                          'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/19961548_10155484269164210_5267146366398589018_n.png?_nc_cat=0&oh=3a264767a1fb51ac1fd97d659b519563&oe=5B7CB8BE')  # the graph api gets this
        self.assertEquals(new_university_object.description,
                          "Welcome to UCL, London's leading multidisciplinary university with 11,000 staff and 38,000 students. Our university is a modern, outward-looking institution, committed to engaging with the major issues of our times. One of the world’s leading multidisciplinary universities, UCL today is a true academic powerhouse.\n\nUCL is among the world's top universities, as reflected in performance in a range of rankings and tables. \n\nWe have a global reach and global vision. Almost two-thirds of our student body come from outside the UK, attracted from 150 countries around the globe. \n\nUCL was founded in 1826 to open up university education in England to those who had been excluded from it. In 1878, it became the first university in England to admit women students on equal terms with men.")  # page public content access, can get this with the api

    def test_add_new_university_society(self):
        # a form is filled in with the:
        uni = Universities.objects.filter(name='Ziferblat Worldwide').first()
        print(uni)

        new_uni_soc_data = {
            'university': uni.id,
            # https://github.com/adbeskine/TOPAIMS_LIVE/blob/master/home/tests/test_purchase_order_view.py line 24, modelchoicefield.
            'facebook_id': 'ZiferblatLondon',
        }

        # the form data is posted to the 'new_university_society' function
        self.client.post(reverse('add_university_society'), data=new_uni_soc_data)

        # the database is updated with the university_society and all it's corect information
        new_uni_soc = Universities_Societies.objects.filter(name='Ziferblat London').first()

        self.assertEquals(new_uni_soc.uni_fk, Universities.objects.filter(name='Ziferblat Worldwide').first())
        self.assertEquals(new_uni_soc.fb_id, '435647379890134')
        self.assertEquals(new_uni_soc.name, 'Ziferblat London')
        self.assertEquals(new_uni_soc.cover_photo,
                          'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/10347161_576476745807196_4053901167283941850_n.jpg?_nc_cat=0&oh=25079da942668dc218f5f607f1a67e86&oe=5B4F3679')
        self.assertEquals(new_uni_soc.description, "Ziferblat is a place where everyone can feel at home. Here you are free to be yourself; you can work, do some art, read a book, play piano, get acquainted with good people, attend events, drink as much tea or coffee as you want — in other words, do whatever you like as long as you respect the space and the other people in it.\n\nZiferblat’s doors are open to everyone. Each Ziferblat guest becomes a sort of micro-tenant of the space, responsible for it and able to influence its life. \n\nYou will be welcomed by the Zifferblat community and able to work with them to help create, supply and develop this project. \n\nEverything is free inside except the time you spend there; and by paying for the time you’ll be making a donation towards the further development of this social experiment.\n\nIf you want to hire out the whole space for private events and functions, send us an email at: ziferblat.london@gmail.com or call us on 07984693440 to negotiate a price.")
        self.assertEquals(new_uni_soc.about, " Ziferblat is a pay-per-minute co-working & social space \n\n£4.20 for 1 hour\n£6.60 for 2 hours \n£9.00 for 3 hours\n\nAfter 4 hours our daily cap starts at £11.40")
        self.assertEquals(new_uni_soc.phone, '07707 901 882')
        self.assertEquals(new_uni_soc.web_site, 'http://london.ziferblat.net/')
        self.assertEquals(new_uni_soc.address, "388 Old Street")

    def test_add_new_event(
            self):  # currently on the facebook graph api, all calls to an event not made by, or rsvp'd to by the caller returns an empty list
        # a form is filled in with the:

        uni_soc = Universities_Societies.objects.filter(name='Ziferblat Kiev').first()

        new_event_data = {
            'title': 'CASTLE Wintersfest Party',
            'date': datetime.date.today(),
            'time': datetime.time(7, 15),
            'address': 'no.10 awesome street, Kyiv',
            'tickets': 'Tickets are not needed for this event',
            'uni_soc': uni_soc.id,
            'cover_photo': 'https://cover_photo_url_goes_here',
            'description': 'The social highlight of the year in Kyiv and London',
        }

        # the form data is posted to the 'new_event' function
        self.client.post(reverse('add_event'), data=new_event_data)

        # the database is updated with the Event and all it's corect information
        new_event_object = Events.objects.filter(title='CASTLE Wintersfest Party').first()

        self.assertEquals(new_event_object.title, 'CASTLE Wintersfest Party')
        self.assertEquals(new_event_object.date, datetime.date.today())
        self.assertEquals(new_event_object.time, datetime.time(7, 15))
        self.assertEquals(new_event_object.address, 'no.10 awesome street, Kyiv')
        self.assertEquals(new_event_object.tickets, 'Tickets are not needed for this event')
        self.assertEquals(new_event_object.uni_socs,
                          Universities_Societies.objects.filter(name='Ziferblat Kiev').first())
        self.assertEquals(new_event_object.cover_photo, 'https://cover_photo_url_goes_here')
        self.assertEquals(new_event_object.description, 'The social highlight of the year in Kyiv and London')
