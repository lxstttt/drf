from django.db import models

# Create your models here.


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:

        abstract = True

class InClass(BaseModel):

    cl_name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        db_table = 'stu_class'
        verbose_name = "班级表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cl_name

class Student(BaseModel):

    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other"),
    )

    stu_name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.SmallIntegerField(choices=gender_choices,default=0)
    pic = models.ImageField(upload_to='pic', default='pic/1.jpg')
    in_class = models.OneToOneField(to='InClass',on_delete=models.CASCADE,related_name='student')

    class Meta:
        db_table = 'student'
        verbose_name = "学生表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stu_name
