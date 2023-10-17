"""
Module that holds the models for 'restaurants' app
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Restaurant(models.Model):
    """
    Class that represents a restaurant.

    This model encapsulates information about a restaurant, 
    including its unique ID, owner, name, and URL slug.

    Attributes:
        id (AutoField): Unique identifier for the restaurant.
        owner (ForeignKey): The user who owns the restaurant.
        name (str): The name of the restaurant.
        slug (str): The URL-friendly slug for the restaurant.

    Methods:
        __str__(): Returns the name of the restaurant.
        save(): Overrides the save method to update the slug 
        based on the name before saving.
    """
    id = models.AutoField(
        verbose_name="Restaurant's ID",
        primary_key=True,
        auto_created=True)
    owner = models.ForeignKey(
        verbose_name="Owner",
        to=User,
        on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Name", max_length=100)
    slug = models.SlugField(verbose_name="Restaurant's URL", max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """
        Defines extra data for the model like the name to show on the admin's page
        """
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    # Override save method to update slug field before save
    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        self.slug = slugify(self.name)
        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
