from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length =  40)

    def __str__(self): # show actual city name
        return self.name

    class Meta:
        verbose_name_plural = 'sities'
