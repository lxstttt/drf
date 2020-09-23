from django.db import models

# Create your models here.
class Tree(models.Model):

    name = models.CharField(max_length=50 , verbose_name='树名')
    age = models.IntegerField()
    kind = models.CharField(max_length=100 , verbose_name='树种')

    class Meta:
        db_table = 'tree'
        verbose_name = '树先生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name