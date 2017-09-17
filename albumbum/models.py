from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Album(models.Model):
    user = models.ForeignKey(User)
    nazwa_albumu = models.CharField(max_length=500, default="nazwa Albumu")
    temat = models.CharField(max_length=100, default="temat")
    opis_albumu = models.TextField(max_length=2000, default="opis")
    album_logo = models.CharField(max_length=1000, default="link http:// do logo")

    def get_absolute_url(self):
        return reverse('albumbum:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nazwa_albumu + ' - ' + str(self.user)


class Foto(models.Model):
    albumnr = models.ForeignKey(Album, on_delete=models.CASCADE)
    nazwa_foto = models.CharField(max_length=250, default='nazawa foto')
    obraz = models.CharField(max_length=1000, default='link http:// do obrazu')

    def __str__(self):
        return self.nazwa_foto
