from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'albumbum'

urlpatterns = [
    # /albumbum/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /albumbum/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /albumbum/login_user/
    url(r'^login_user/$', views.login_user, name='login_user'),

    # /albumbum/logout_user/
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # /albumbum/<albumbum.id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /albumbum//albumadd/
    url(r'albumadd/$', views.AlbumCreate.as_view(), name='album-add'),

    # /albumbum//update/2/
    url(r'update/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='albumbum-update'),

    # /albumbum//delete/2/
    url(r'delete/(?P<pk>[0-9]+)/$', views.AlbumDelete.as_view(), name='albumbum-delete'),

    # /albumbum//2/fotoadd
    url(r'^(?P<pk>[0-9]+)/fotoadd/$', views.FotoCreate.as_view(), name='foto-add'),

    # /albumbum//2/fotoadd
    url(r'^(?P<pk>[0-9]+)/fotodelete/$', views.FotoDelete.as_view(), name='foto-delete'),

    # /albumbum//2/fotoupdate
    url(r'^(?P<pk>[0-9]+)/fotoupdate/$', views.FotoUpdate.as_view(), name='foto-update'),

 ]
