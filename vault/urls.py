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

urlpatterns = patterns('vault.views',
    url(r'^$', 'index', name='vault.index'),
    url(r'^groups/(?P<uuid>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$', 'group',
        name='vault.group'),
    url(r'^setkey/$', 'set_key', name='vault.set_key'),
    url(r'^lock/$', 'lock_session', name='vault.lock_session'),
    url(r'^genpass/$', 'random_password', name='vault.random_password'),
    url(r'^checksession/$', 'check_session', name='vault.check_session'),
)
