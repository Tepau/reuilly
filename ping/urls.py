from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'reuillytt'

urlpatterns = [

    url(r'^horaires/$', views.horaires.as_view(), name='horaires'),
    url(r'^inscription/$', views.inscription, name='inscription'),
    url(r'^liens/$', views.liens.as_view(), name='liens'),
    url(r'^historique/$', views.Historique.as_view(), name='historique'),
    url(r'^connexion/$', views.connexion, name='connexion'),
    url(r'^deconnexion/$', LogoutView.as_view(next_page='index'), name='deconnexion'),
    url(r'^moncompte/$', views.account, name='moncompte'),
    url(r'^photo/$', views.photo, name='photo'),
    url(r'^supprimerphoto/$', views.supprimerphoto, name='supprimerphoto'),
    url(r'^creation/$', views.creation, name='creation'),
    url(r'^mentions/$', views.Mentions.as_view(), name='mentions'),
    url(r'^cgu/$', views.Cgu.as_view(), name='cgu'),
    url(r'^ping/$', views.ping, name='ping'),
    url(r'^ping2/$', views.ping2, name='ping2'),

]

