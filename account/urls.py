from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^profile/$', views.profileView.as_view(template_name='account/profile.html'), name='profile'),
	url(r'^info/$', views.info, name='info'),
	url(r'^info/info_change/$', views.info_change, name='info_change'),
	url(r'^contact_us/$', views.contact_us, {'template_name': 'account/contact_us.html'}, name='contact_us'),
]
