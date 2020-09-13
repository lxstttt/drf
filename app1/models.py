from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    pwd = models.CharField(max_length=40)
    email = models.CharField(max_length=100)

    class Meta:
        db_table = 'show_user'