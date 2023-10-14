from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    id=models.AutoField(verbose_name="Restaurant's ID", primary_key=True, auto_created=True)
    owner=models.ForeignKey(verbose_name="Owner", to=User, on_delete=models.PROTECT)
    name=models.CharField(verbose_name="Name", max_length=100)
    slug=models.SlugField(verbose_name="Restaurant's URL", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Restaurant"
        verbose_name_plural="Restaurants"