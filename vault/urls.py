from django.conf.urls import patterns, url

urlpatterns = patterns('vault.views',
    url(r'^$', 'index', name='vault.index'),
    url(r'^groups/(?P<uuid>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$', 'group',
        name='vault.group'),
    url(r'^setkey/$', 'set_key', name='vault.set_key'),
    url(r'^lock/$', 'lock_session', name='vault.lock_session'),
    url(r'^genpass/$', 'random_password', name='vault.random_password'),
)
