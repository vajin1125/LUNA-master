from django.http import HttpResponse

import json

from Uni_Socs.models import Universities_Societies
from Users.models import LunaUsers


# this app has all the LUNA profiles stored here, users following of uni societies + other user/ UI information/settings

# ###### HELP Function ######
def check_security_key(original_json_data, user): # POSTMVP make this a proper decorator
    # MVP - to be added before every HttpResponse, simply checks the user's security key is the same as in the db
    # for continue or redirect to login
    if original_json_data['user_security_key'][0]['key'] == user.security_key:
        pass
    else:
        return 'security fail'


def update_socx_id(i, uni_socs_id, user_id):
    if i == 'soc1_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc1_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc2_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc2_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc3_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc3_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc4_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc4_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc5_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc5_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc6_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc6_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc7_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc7_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc8_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc8_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc9_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc9_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save()
    elif i == 'soc10_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc10_id = Universities_Societies.objects.filter(id=uni_socs_id).first().id

        obj.save() # makes soci_id the uni_socs_id


def update_socx_id_none(i, user_id):
    if i == 'soc1_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc1_id = None

        obj.save()
    elif i == 'soc2_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc2_id = None

        obj.save()
    elif i == 'soc3_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc3_id = None

        obj.save()
    elif i == 'soc4_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc4_id = None

        obj.save()
    elif i == 'soc5_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc5_id = None

        obj.save()
    elif i == 'soc6_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc6_id = None

        obj.save()
    elif i == 'soc7_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc7_id = None

        obj.save()
    elif i == 'soc8_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc8_id = None

        obj.save()
    elif i == 'soc9_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc9_id = None

        obj.save()
    elif i == 'soc10_id':
        obj = LunaUsers.objects.filter(id=user_id).first()
        obj.soc10_id = None

        obj.save() # makes soci_id None

##########################################



def follow_university_societies(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        user_pk = json_data['user'][0]['user_id']
        user = LunaUsers.objects.filter(pk=user_pk).first()

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

    user.soc1 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc1']).first()
    user.soc2 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc2']).first()
    user.soc3 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc3']).first()
    user.soc4 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc4']).first()
    user.soc5 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc5']).first()
    user.soc6 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc6']).first()
    user.soc7 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc7']).first()
    user.soc8 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc8']).first()
    user.soc9 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc9']).first()
    user.soc10 = Universities_Societies.objects.filter(pk=json_data['uni_socs_selection'][0]['soc10']).first()

    user.save()

    return HttpResponse('Successfully updated')


def toggle_On(request):
    json_data = json.loads(request.body)

    user_id = json_data['user'][0]['user_id']

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

    user_following_clubs_list_of_queries = LunaUsers.objects.filter(id=user.id).values('soc1_id', 'soc2_id', 'soc3_id',
                                                                                       'soc4_id', 'soc5_id', 'soc6_id',
                                                                                       'soc7_id', 'soc8_id', 'soc9_id',
                                                                                       'soc10_id')
    for instance in user_following_clubs_list_of_queries:
        for i in instance:
            if instance[i] is None:
                uni_socs_id = json_data['uni_socs_selection'][0]['soc_id']
                update_socx_id(i, uni_socs_id, user_id)

                return HttpResponse('Done')

        print('yes')
        data = {}
        data['response'] = []
        data['response'].append({
            'get_response': 'reached society following limit'
        })
        response_data = json.dumps(data)

       
        return HttpResponse(response_data)


def toggle_Off(request):
    json_data = json.loads(request.body)

    user_id = json_data['user'][0]['user_id']
    uni_socs_id = json_data['uni_socs_selection'][0]['soc_id']

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
    user_following_clubs_list_of_queries = LunaUsers.objects.filter(id=user.id).values('soc1_id', 'soc2_id', 'soc3_id',
                                                                                       'soc4_id', 'soc5_id', 'soc6_id',
                                                                                       'soc7_id', 'soc8_id', 'soc9_id',
                                                                                       'soc10_id')
    new_uni_socs_id = Universities_Societies.objects.filter(id=uni_socs_id).first()

    for instance in user_following_clubs_list_of_queries:
        for i in instance:
            if instance[i] is not None:
                if instance[i] == new_uni_socs_id.id:

                    update_socx_id_none(i, user.id)
                    break

    return HttpResponse('Done')


def user_profile(request):
    json_data = json.loads(request.body)
    user_id = json_data['user_profile_request'][0]['user_id']

    user = LunaUsers.objects.filter(id=user_id).first()

    ########### security check ###############

    if check_security_key(json_data, user) == 'security fail':
    
        data={}
        data['response'] = []
        data['response'].append({
            'response': 'security fail'
        })
        response_data = json.dumps(data)

        return HttpResponse(json_data)

    ###########################################

    data = LunaUsers.objects.filter(id=user.id).values('soc1_id', 'soc2_id', 'soc3_id', 'soc4_id',
                                                       'soc5_id', 'soc6_id', 'soc7_id', 'soc8_id',
                                                       'soc9_id', 'soc10_id').first()

    uni_socs_queryset = Universities_Societies.objects.none()

    for instance in data:
        if data[instance] is not None:

            uni_socs_queryset = uni_socs_queryset.union(Universities_Societies.objects.filter(id=data[instance]))

    sorted_by_id_uni_soc_queryset = uni_socs_queryset.order_by('id')

    all_data = {}
    all_data['followed_user_uni_soc'] = []

    for i in sorted_by_id_uni_soc_queryset:
        all_data['followed_user_uni_soc'].append({
            'uni_soc_id': i.id,
            'uni_soc_name': i.name,
            'uni_soc_cover_photo': i.cover_photo,

        })

    json_data = json.dumps(all_data)
    return HttpResponse(json_data)
