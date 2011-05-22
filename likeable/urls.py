#
# django-likeable
#
# See LICENSE for licensing details.
#

from django.conf.urls.defaults import *
from views import like_ajax, like_noajax, like_autodetect


urlpatterns = patterns('',
    url(r'^(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_autodetect, name='likeable_like'),
    url(r'^noajax/(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_noajax, name='likeable_noajax_like'),
    url(r'^ajax/(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_ajax, name='likeable_ajax_like'),
)

