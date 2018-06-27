from django.http import HttpResponse

import json

from Users.models import LunaUsers
from Uni_Socs.models import Universities_Societies

from Users.views import check_security_key


# ###### HELPER Function ######
def check_user_is_following_uni_soc(user_id, soc):
    # Проверка на те uni_soc которые пользователь подписан,
    # Если подписан то возвращаем 'YES'
    data = LunaUsers.objects.filter(id=user_id).values('soc1_id', 'soc2_id', 'soc3_id', 'soc4_id',
                                                       'soc5_id', 'soc6_id', 'soc7_id', 'soc8_id',
                                                       'soc9_id', 'soc10_id')
    for instance in data:
        for i in instance:
            if instance[i] is not None:
                if instance[i] == soc:
                    return 'YES'
            else:
                pass
    return 'NO'


def show_all_uni_socs(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        uni_id = json_data['uni_socs_query'][0]['uni_id']
        user_id = json_data['uni_socs_query'][0]['user_id']

        #########
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

        get_all_uni_soc_from_db = Universities_Societies.objects.filter(uni_fk=uni_id)

        data = {}
        data['uni_socs'] = []

        for i in get_all_uni_soc_from_db:
            data['uni_socs'].append({
                'name': i.name,
                'id': i.id,
                'cover_photo': i.cover_photo,
                'follow': check_user_is_following_uni_soc(user_id, i.id)
            })

        new_data_json = json.dumps(data)

        return HttpResponse(new_data_json)
