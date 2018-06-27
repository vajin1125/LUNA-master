from django import forms
from Uni_Socs.models import Universities, Universities_Societies




class new_university_form(forms.Form):
    domain = forms.CharField()
    uni_facebook_id = forms.CharField()


class new_uni_soc_form(forms.Form):
    university = forms.ModelChoiceField(queryset=Universities.objects.all())
    facebook_id = forms.CharField()


class new_event(forms.Form):
    uni_soc = forms.ModelChoiceField(queryset=Universities_Societies.objects.all())
    title = forms.CharField()
    date = forms.DateField(widget = forms.SelectDateWidget())
    time = forms.TimeField()
    address = forms.CharField()  # required = false? if empty system assumes it is same adress as unisoc?
    tickets = forms.CharField()
    cover_photo = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
