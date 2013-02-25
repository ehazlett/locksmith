from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'login', name='accounts.login'),
    url(r'^logout/$', 'logout', name='accounts.logout'),
    url(r'^details/$', 'details', name='accounts.details'),
    url(r'^signup/$', 'signup', name='accounts.signup'),
    url(r'^activate/$', 'activate', name='accounts.activate'),
    url(r'^hook/$', 'hook', name='accounts.hook'),
)
