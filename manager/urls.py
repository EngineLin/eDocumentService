from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^event_list/(?P<action>\w+)/$', views.event_list, name='event_list'),
	url(r'^org_manage/$', views.org_manage, name='org_manage'),
	url(r'^statistics/$', views.statistics, name='statistics'),
]
