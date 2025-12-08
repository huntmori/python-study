from django.db import models
from django.urls import reverse


# Create your models here.
class MyModelName(models.Model):

    #Fields
    my_field_name = models.CharField(
        max_length=20,
        help_text='Enter field documentation'
    )

    # Meta Data
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

