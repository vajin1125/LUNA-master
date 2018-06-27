from django.db import models
from django.utils import timezone
import datetime


# ########### HELPER METHOD ###########
def convert_to_date(str_date, form='%Y-%m-%d'):
    dt = datetime.datetime.strptime(str_date, form)
    return dt.date()


def convert_to_time(str_time, form='%H:%M:%S'):
    dt = datetime.datetime.strptime(str_time, form)
    return dt.time()


class Universities(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=30, default='@test_uni.com')
    uni_facebook_id = models.CharField(max_length=100,  null=True)
    cover_photo = models.CharField(max_length=500, null=True)
    description = models.TextField(max_length=100000, null=True)

    def __str__(self):
        return self.name


class Universities_Societies(models.Model):
    name = models.CharField(max_length=200, null=True)
    uni_fk = models.ForeignKey(Universities, on_delete=models.CASCADE)
    fb_id = models.CharField(max_length=100, default='NO ID PRESENT')               # uni = models.ForeignKey(Universities, on_delete=models.CASCADE, null=True)
    cover_photo = models.CharField(max_length=500, null=True)
    description = models.TextField(max_length=100000, null=True)
    about = models.CharField(max_length=300, null=True) # about and description on facebook pages are two different things, apparently
    web_site = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Events(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=300)
    tickets = models.CharField(max_length=300)
    uni_socs = models.ForeignKey(Universities_Societies, on_delete=models.CASCADE, null=True)
    cover_photo = models.CharField(max_length=500, null=True)
    description = models.TextField(max_length=100000, null=True)
    dateTime = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            if type(self.date) == str:
                self.dateTime = datetime.datetime.combine(convert_to_date(self.date), convert_to_time(self.time))
            else:
                self.dateTime = datetime.datetime.combine(self.date, self.time)
        super(Events, self).save(*args, **kwargs)



