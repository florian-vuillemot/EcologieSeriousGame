from django.db import models

# Create your models here.
class Maison(models.Model):
    toit = models.ImageField(default='toit.jpg')
    mur = models.ImageField()
    porte = models.ImageField()
