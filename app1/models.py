from django.db import models

# Create your models here.
class User(models.Model):

    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other"),
    )

    username = models.CharField(max_length=60)
    pwd = models.CharField(max_length=60)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    email = models.CharField(max_length=60)
    pic = models.ImageField(upload_to='pic', default='pic/1.jpg')

    class Meta:
        db_table = 'kk_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username