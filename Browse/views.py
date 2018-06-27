from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json
import datetime


from Users.models import LunaUsers, RSVP_event
from Uni_Socs.models import Events, Universities_Societies

from Users.views import check_security_key


# HELP METHOD
def convert_to_date(str_date, form='%Y-%m-%d'):
    dt = datetime.datetime.strptime(str_date, form)
    return dt.date()


def feed(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # Get User ID from JSON
        user_id = json_data['request_homepage_events_feed'][0]['user_id']

        user = LunaUsers.objects.filter(id=user_id).first()
        
        ########### security check ###############

        if check_security_key(json_data, user) == 'security fail':
    
            data={}
            data['response'] = []
            data['response'].append({
                'response': 'security fail'
            })
            response_data = json.dumps(data)

            return HttpResponse(response_data)

        ###########################################

        # Query the database
        data = LunaUsers.objects.filter(id=user_id).values('soc1_id', 'soc2_id', 'soc3_id', 'soc4_id',
                                                           'soc5_id', 'soc6_id', 'soc7_id', 'soc8_id',
                                                           'soc9_id', 'soc10_id')

        merged_unsorted_queryset = Events.objects.none()   # this makes an empty queryset

        for instance in data:
            for i in instance:
                if instance[i] is not None:
                    merged_unsorted_queryset = merged_unsorted_queryset.union(Events.objects.filter(uni_socs=instance[i]))  # all the different querysets merge with the empty querysets to form one queryeset - .orderd_by can now be used

        # sorted_id_objects = id_objects_events.

        id_objects_events = merged_unsorted_queryset.order_by('dateTime')
        all_data = {}
        all_data['event'] = []

        for i in id_objects_events:
            print(i.dateTime)
            all_data['event'].append({
                'title': i.title,
                'cover_photo': i.cover_photo,
                'date': i.date,
                'time': i.time,
                'address': i.address,
                'id': i.id,
            })

        json_data = json.dumps(all_data, cls=DjangoJSONEncoder)

        return HttpResponse(json_data)


def event_page(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        user_id = json_data['event_page_request'][0]['user_id']
        event = json_data['event_page_request'][0]['event_id']

        get_event = Events.objects.filter(id=event).first()
        user = LunaUsers.objects.filter(id=user_id).first()

        ########### security check ###############

        if check_security_key(json_data, user) == 'security fail':
    
            data={}
            data['response'] = []
            data['response'].append({
                'response': 'security fail'
            })
            response_data = json.dumps(data)

            return HttpResponse(response_data)

        ###########################################

        data = {}
        data['event'] = []
        data['event'].append({
            'title': get_event.title,
            'date': get_event.date,
            'description': get_event.description,
            'time': get_event.time,
            'address': get_event.address,
            'tickets': get_event.tickets,
            'event_cover_photo': get_event.cover_photo,
            'club_cover_photo': get_event.uni_socs.cover_photo,
            'event_id': get_event.id,
            'club_id': get_event.uni_socs.id,
            'status': RSVP_event.objects.filter(user=user, event=get_event).first().status

        })

        json_data = json.dumps(data, cls=DjangoJSONEncoder)

        return HttpResponse(json_data)


def rsvp_status_change(request):
    if request.method == 'POST':

        json_data = json.loads(request.body)

        user_id = json_data['send_RSVP'][0]['user_id']
        event_id = json_data['send_RSVP'][0]['event_id']
        status = json_data['send_RSVP'][0]['RSVP_event_status']

        ###
        user = LunaUsers.objects.filter(id=user_id).first()
        ########### security check ###############

        if check_security_key(json_data, user) == 'security fail':
    
            data={}
            data['response'] = []
            data['response'].append({
                'response': 'security fail'
            })
            response_data = json.dumps(data)

            return HttpResponse(response_data)

        ###########################################

        if RSVP_event.objects.filter(user=user_id, event=event_id).first() is not None:

            rsvp = RSVP_event.objects.filter(user=user_id, event=event_id).first()
            rsvp.status = status
            rsvp.save()
    
            return HttpResponse('rsvp updated')

        else:

            RSVP_event.objects.create(user=user_id, event=event_id, status=status)

            return HttpResponse('new rsvp')


def uni_socs_profile(request):
    json_data = json.loads(request.body)

    get_user_id = json_data['uni_soc_profile_page_request'][0]['user_id']
    get_uni_socs_id = json_data['uni_soc_profile_page_request'][0]['uni_socs_id']

    user = LunaUsers.objects.filter(id=get_user_id).first()
    ########### security check ###############

    if check_security_key(json_data, user) == 'security fail':
    
        data={}
        data['response'] = []
        data['response'].append({
            'response': 'security fail'
        })
        response_data = json.dumps(data)

        return HttpResponse(response_data)

    ###########################################

    uni_soc = Universities_Societies.objects.filter(id=get_uni_socs_id).first()
    uni_soc_events = Events.objects.filter(uni_socs=uni_soc.id).order_by('dateTime')

    unmerged_user_following_clubs_list_of_queries = LunaUsers.objects.filter(id=user.id).values('soc1_id', 'soc2_id', 'soc3_id', 'soc4_id',
                                                    'soc5_id', 'soc6_id', 'soc7_id', 'soc8_id',
                                                    'soc9_id', 'soc10_id')

    merged_user_following_clubs_list_of_queries = Universities_Societies.objects.none()   # this makes an empty queryset

    for instance in unmerged_user_following_clubs_list_of_queries:
        for i in instance:
            if instance[i] is not None:
                merged_user_following_clubs_list_of_queries = merged_user_following_clubs_list_of_queries.union(Universities_Societies.objects.filter(id=instance[i]))

    user_follow_status = 'False'

    for i in merged_user_following_clubs_list_of_queries:
        if i.id == get_uni_socs_id:
            user_follow_status = 'True'

            # is 'uni_soc_id' in this queryset? y/n, then send to json
            # user_follow_status = y/n


    data = {}
    data['uni_soc_profile'] = []
    data['uni_soc_profile'].append({
        'name': uni_soc.name,
        'cover_photo': uni_soc.cover_photo,
        'about': uni_soc.about,
        'web_site': uni_soc.web_site,
        'phone': uni_soc.phone,
        'address': uni_soc.address,
        'user_follow_status': user_follow_status
    })

    data['uni_soc_events'] = []
    for i in uni_soc_events[0:5]:
        data['uni_soc_events'].append({
            'title': i.title,
            'cover_photo': i.cover_photo,
            'date': i.date,
            'id':i.id
        })

    json_data = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(json_data)


def uni_soc_profile_all_events(request):
    json_data = json.loads(request.body)

    ########### security check ##############
    user_id = json_data['user_id'][0]['user_id']
    user = LunaUsers.objects.filter(id=user_id).first()
    ########### security check ###############
    
    if check_security_key(json_data, user) == 'security fail':
    
        data={}
        data['response'] = []
        data['response'].append({
            'response': 'security fail'
        })
        response_data = json.dumps(data)

        return HttpResponse(response_data)

    ###########################################

    uni_soc_id = json_data['uni_soc_all_events_page_request'][0]['uni_soc_id']
    uni_soc_events = Events.objects.filter(uni_socs=uni_soc_id).order_by('-date')

    data = {}
    data['uni_soc_all_events'] = []
    for i in uni_soc_events:
        data['uni_soc_all_events'].append({
            'title': i.title,
            'cover_photo': i.cover_photo,
            'date': i.date,
            'id': i.id
        })

    json_data = json.dumps(data, cls=DjangoJSONEncoder)

    return HttpResponse(json_data)


def search_all_event_from_uni(request):
    json_data = json.loads(request.body)

    date_range_1 = json_data['user_all_uni_events_request'][0]['date_range_1']
    date_range_2 = json_data['user_all_uni_events_request'][0]['date_range_2']
    user_id = json_data['user_all_uni_events_request'][0]['user_id']

    user = LunaUsers.objects.filter(id=user_id).first()
    
    ########### security check ###############
    
    if check_security_key(json_data, user) == 'security fail':
    
        data={}
        data['response'] = []
        data['response'].append({
            'response': 'security fail'
        })
        response_data = json.dumps(data)

        return HttpResponse(response_data)

    ###########################################

    all_uni_socs_kpi = Universities_Societies.objects.filter(uni_fk=user.uni).all()

    merged_unsorted_queryset = Events.objects.none()

    for soc in all_uni_socs_kpi:
        merged_unsorted_queryset = merged_unsorted_queryset.union(Events.objects.filter(uni_socs=soc.id))

    if date_range_1 and date_range_2 is not None:
        date_1 = convert_to_date(date_range_1)
        date_2 = convert_to_date(date_range_2)

        date_filtered_queryset = Events.objects.none()

        for event in merged_unsorted_queryset:
            if event.date <= date_2 or event.date >= date_1:
                date_filtered_queryset = date_filtered_queryset.union(Events.objects.filter(id=event.id))

            merged_unsorted_queryset = date_filtered_queryset

    sorted_by_date_queryset = merged_unsorted_queryset.order_by('dateTime')
    print(sorted_by_date_queryset)

    data_all_event_from_uni = {}
    data_all_event_from_uni['all_from_uni_event'] = []

    for i in sorted_by_date_queryset:
        data_all_event_from_uni['all_from_uni_event'].append({
            'cover_photo': i.cover_photo,
            'date': i.date,
            'time': i.time,
            'address': i.address,
            'tickets': i.tickets,
            'description': i.description,
            'id': i.id
        })

    json_data = json.dumps(data_all_event_from_uni, cls=DjangoJSONEncoder)

    return HttpResponse(json_data)


def my_events(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        user_id = json_data['request_for_my_events'][0]['user_id']

        user = LunaUsers.objects.filter(id=user_id).first()
        ########### security check ###############
    
        if check_security_key(json_data, user) == 'security fail':
    
            data={}
            data['response'] = []
            data['response'].append({
                'response': 'security fail'
            })
            response_data = json.dumps(data)

            return HttpResponse(response_data)

        ###########################################

        rsvp_data = RSVP_event.objects.filter(user=user_id, status='YES')
        merged_unsorted_queryset = Events.objects.none()

        for i in rsvp_data:
            merged_unsorted_queryset = merged_unsorted_queryset.union(Events.objects.filter(id=i.event.id))

        sorted_id_objects = merged_unsorted_queryset.order_by('dateTime')

        all_data = {}
        all_data['my_events'] = []

        for i in sorted_id_objects:
            all_data['my_events'].append({
                'cover_photo': i.cover_photo,
                'date': i.date,
                'time': i.time,
                'address': i.address,
                'id': i.id,
            })

        json_data = json.dumps(all_data, cls=DjangoJSONEncoder)

        return HttpResponse(json_data)
