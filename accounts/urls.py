# Copyright 2013 Evan Hazlett and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'login', name='accounts.login'),
    url(r'^logout/$', 'logout', name='accounts.logout'),
    url(r'^details/$', 'details', name='accounts.details'),
    url(r'^signup/$', 'signup', name='accounts.signup'),
    url(r'^confirm/(?P<code>[\W,\w]+)/$', 'confirm', name='accounts.confirm'),
    url(r'^activate/$', 'activate', name='accounts.activate'),
    url(r'^hook/$', 'hook', name='accounts.hook'),
)
