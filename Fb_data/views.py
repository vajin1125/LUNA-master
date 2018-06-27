from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .forms import new_university_form, new_uni_soc_form, new_event

from Uni_Socs.models import Universities, Universities_Societies, Events
from LUNA_API.settings import FB_APP_TOKEN as at

import requests


def send_graph_api_request(facebook_id, fields_list, at=at):
    fields = '?fields='

    for field in fields_list:
        fields = fields + field + ','

    fields = fields[:-1]
    return requests.get(f'https://graph.facebook.com/v3.0/{facebook_id}{fields}&access_token={at}').json()


def get_all_university_information(uni_facebook_id):
    # Name
    # cover photo
    # desctiption

    json_response = send_graph_api_request(uni_facebook_id, fields_list=['name', 'picture', 'description'])

    name = json_response['name']
    picture = json_response['picture']['data']['url']
    description = json_response['description']
    fbid = json_response['id']

    uni_info = {'name': name, 'picture': picture, 'description': description, 'fbid': fbid}

    return uni_info


def add_university(request):
    if request.method == 'POST':
        form = new_university_form(request.POST)

        if form.is_valid():
            domain = form.cleaned_data['domain']
            uni_facebook_id = form.cleaned_data['uni_facebook_id']

            uni_info = get_all_university_information(uni_facebook_id=uni_facebook_id)
            name = uni_info['name']
            cover_photo = uni_info['picture']
            description = uni_info['description']
            fbid = uni_info['fbid']

            Universities.objects.create(
                name=name,
                domain=domain,
                uni_facebook_id=fbid,
                cover_photo=cover_photo,
                description=description,
            )

            return (HttpResponseRedirect(reverse('data_entry_interface')))  # needs to flash a confirmation notification on the front end

        else:
            print(form.errors)


def get_all_university_society_information(request, uni_soc_facebook_id):
    data_json = send_graph_api_request(uni_soc_facebook_id,
                                  fields_list=['name', 'picture', 'description', 'about', 'phone', 'website',
                                               'location'])


    name = data_json['name']
    picture = data_json['picture']['data']['url']
    description = data_json['description']
    about = data_json['about']
    phone = data_json['phone']
    website = data_json['website']
    address = data_json['location']['street']
    fbid = data_json['id']

    uni_soc_info = {
        'name': name,
        'picture': picture,
        'description': description,
        'about': about,
        'phone': phone,
        'website': website,
        'address': address,
        'fbid': fbid,
    }

    return uni_soc_info


def add_university_society(request):
    if request.method == 'POST':
        form = new_uni_soc_form(request.POST)

        if form.is_valid():
            university_id = form.cleaned_data['university']
            uni_soc_fb_id = form.cleaned_data['facebook_id']

            uni_soc_info = get_all_university_society_information(request, uni_soc_fb_id)

            Universities_Societies.objects.create(
                uni_fk=university_id,
                name=uni_soc_info['name'],
                fb_id=uni_soc_info['fbid'],
                cover_photo=uni_soc_info['picture'],
                description=uni_soc_info['description'],
                about=uni_soc_info['about'],
                web_site=uni_soc_info['website'],
                phone=uni_soc_info['phone'],
                address=uni_soc_info['address'],
            )

            return HttpResponseRedirect(reverse('data_entry_interface'))

        else:
            print(form.errors)


def add_event(request):
    if request.method == 'POST':
        form = new_event(request.POST)

        if form.is_valid():

            Events.objects.create(
                title=form.cleaned_data['title'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                address=form.cleaned_data['address'],
                tickets=form.cleaned_data['tickets'],
                uni_socs=form.cleaned_data['uni_soc'],
                cover_photo=form.cleaned_data['cover_photo'],
                description=form.cleaned_data['description'],
            )

            return HttpResponseRedirect(reverse('data_entry_interface'))

        else:
            print(form.errors)


# def get_all_event_information(request):
# the event api endpoint has been turned off by facebook!!!
# if it is turned back on again, we need to run this twice a day on all the uni societies


def data_entry_interface(request):
    context = {
        'new_university_form': new_university_form,
        'new_uni_soc_form': new_uni_soc_form,
        'new_event_form': new_event,
    }

    return render(request, 'Fb_data/input.html', context=context)
