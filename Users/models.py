from django.db import models

from Uni_Socs.models import Universities, Universities_Societies, Events


class LunaUsers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    fb_id = models.CharField(max_length=500)
    security_key = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    uni = models.ForeignKey(Universities, on_delete=models.CASCADE, null=True)
    verification_key = models.CharField(max_length=100, null=True)

    #when security key fails, signal is sent back saying 'security fail', make front end api then send signal to api
    # to check verification status, if unverified, 
    # send user to email page where they can change their email/resend the confirmation email
    # new backend function(s) needed to resend email/change email/start registration again for user

    soc1 = models.ForeignKey(Universities_Societies, related_name='soc1', null=True, on_delete=models.CASCADE)
    soc2 = models.ForeignKey(Universities_Societies, related_name='soc2', null=True, on_delete=models.CASCADE)
    soc3 = models.ForeignKey(Universities_Societies, related_name='soc3', null=True, on_delete=models.CASCADE)
    soc4 = models.ForeignKey(Universities_Societies, related_name='soc4', null=True, on_delete=models.CASCADE)
    soc5 = models.ForeignKey(Universities_Societies, related_name='soc5', null=True, on_delete=models.CASCADE)
    soc6 = models.ForeignKey(Universities_Societies, related_name='soc6', null=True, on_delete=models.CASCADE)
    soc7 = models.ForeignKey(Universities_Societies, related_name='soc7', null=True, on_delete=models.CASCADE)
    soc8 = models.ForeignKey(Universities_Societies, related_name='soc8', null=True, on_delete=models.CASCADE)
    soc9 = models.ForeignKey(Universities_Societies, related_name='soc9', null=True, on_delete=models.CASCADE)
    soc10 = models.ForeignKey(Universities_Societies, related_name='soc10', null=True, on_delete=models.CASCADE)


class RSVP_event(models.Model):      # события, на которые они решили пойти
    user = models.ForeignKey(LunaUsers, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, null=True)     # always either 'YES', 'NO', 'INTERESTED' or 'UNDEFINED'
