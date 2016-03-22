from django.conf.urls import url
from Apollo.views import *

urlpatterns = [
    #Authentication
    url(r'^register$', register, name="register"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name="login"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    #Private Access(Doctors)
    url(r'^home$', home, name="home"),
    url(r'^tent$', tent, name="tent"),
    url(r'^patient$', patient, name="patient"),
    url(r'^priority$', priority, name="priority"),
    url(r'^check$', check, name="check"),
    url(r'^checkin$', checkin, name="checkin"),
    url(r'^prioritize$', prioritize, name="prioritize"),
    url(r'^patient_media/(?P<id>\d+)$$', patient_media, name="patient_media"),
    url(r'^injury_media/(?P<id>\d+)$$', injury_media, name="injury_media"),
    #From device
    url(r'^create$', create, name="create"),
    #Public Access(Everyone)
    url(r'^$', index, name="index"),
    url(r'^identify$', identify, name="identify"),
    url(r'^id_person$', id_person, name="id_person"),
    url(r'^statistics$', statistics, name="statistics")
]