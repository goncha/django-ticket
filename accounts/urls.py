from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
   url(r'^$', 'home_view', name='home'),
   url(r'^login/$', 'login_view', name='login'),
   url(r'^logout/$', 'logout_view', name='logout'),
   url(r'^register/$', 'register_view', name='register'),
   url(r'^password/$', 'password_view', name='password'),
   url(r'^profile/$', 'profile_view', name='profile'),
   url(r'^hello/$', 'hello_view', name='hello'),
)
