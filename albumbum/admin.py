from django.contrib import admin

# Register your models here.

from .models import Album, Foto


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'nazwa_albumu', 'user']

    class Meta:
        model = Album
admin.site.register(Album, AlbumAdmin)


class FotoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'nazwa_foto', 'albumnr']

    class Foto:
        model = Foto
admin.site.register(Foto, FotoAdmin)
