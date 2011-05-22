#
# django-likeable
#
# See LICENSE for licensing details.
#

from django.conf.urls.defaults import *
from views import like_ajax, like_noajax, like_autodetect


urlpatterns = patterns('',
    (r'^(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_autodetect),
    (r'^noajax/(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_noajax),
    (r'^ajax/(?P<content_type_id>\d+)/(?P<object_id>\d+)', like_ajax),
)

