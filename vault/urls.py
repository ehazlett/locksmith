from django.conf.urls import patterns, url

urlpatterns = patterns('vault.views',
    url(r'^$', 'index', name='vault.index'),
    url(r'^group/add/$', 'add_credential_group',
        name='vault.add_credential_group'),
    url(r'^groups/(?P<uuid>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$', 'group',
        name='vault.group'),
)
