
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    gender_choices = (
        (0, "男"),
        (1, "女"),
        (2, "未知"),
    )

    users_name = models.CharField(max_length=80)
    real_name = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    gender = models.SmallIntegerField(default=0, choices=gender_choices)
    status = models.SmallIntegerField(default=False)
    register_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bz_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Employee(models.Model):
    emp_name = models.CharField(max_length=80)
    img = models.ImageField(upload_to='pic', default="pic/1.jpg")
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    age = models.IntegerField()

    class Meta:
        db_table = "bz_employee"
        verbose_name = "员工表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.emp_name
