from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^page/(?P<pk>\d+)$', views.page_detail, name='page_detail'),
    url(r'^my_pages/$', views.my_pages, name='my_pages'),
    # url(r'^search/$', views.SearchListView.as_view(), name='search_list_view'),
    url(r'^pages/$', views.PageListView.as_view(), name='page_list'),
    url(r'^event/create/(?P<xy>\d+)$', views.EventCreate.as_view(), name='create_event'),
    url(r'^deadline/create/(?P<xy>\d+)$', views.DeadlineCreate.as_view(), name='create_deadline'),
    url(r'^student/create/page/$', views.CreatePage, name='createpage'),
    url(r'^student/create/$', views.StudentCreate.as_view(), name='student_create'),
    url(r'^appkey$', views.appkey, name='appkey'),
    url(r'^subscribe/(?P<pk>\d+)$', views.subscribe, name='subscribe'),
    url(r'^list$', views.listing, name='list'),
    url(r'^events$', views.event_app, name='event_app'),
    url(r'^deadlines$', views.deadlines_app, name='deadlines_app'),
    
]

