from django.db import models

# Create your models here.

class Communes(models.Model):
    commune_name = models.CharField(max_length=200)

    def __str__(self):
        return self.commune_name