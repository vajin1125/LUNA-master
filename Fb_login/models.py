from django.db import models
from Users.models import LunaUsers
# Create your models here.

# fb access tokens go here. connect to users with foreign key.


class Access_Tokens(models.Model):

	User = models.ForeignKey(LunaUsers, on_delete=models.CASCADE)
	access_token = models.CharField(max_length=550)
