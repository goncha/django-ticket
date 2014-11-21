from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
   url(r'^$', 'home', name='home'),
   url(r'^login/$', 'login', name='login'),
   url(r'^logout/$', 'logout', name='logout'),
   url(r'^register/$', 'register', name='register'),
   url(r'^password/$', 'password', name='password'),
   url(r'^profile/$', 'profile', name='profile'),
   url(r'^hello/$', 'hello', name='hello'),
)
