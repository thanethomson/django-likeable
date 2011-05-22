#
# django-likeable
#
# See LICENSE for licensing details.
#

try:
    import json
except ImportError:
    import simplejson as json

from models import Like
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import settings

from urlparse import urlparse
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect



def like(request, content_type_id, object_id):
    """
    The function which generates the like for the given object.
    """

    content_type = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(content_type.model_class(), pk=object_id)

    # generate a like by this user for the content object
    like = Like.objects.create(user=request.user, liked=obj)




def generate_back_url(request, default=settings.DEFAULT_LIKE_BACK_URL):
    """
    Inspired by http://stackoverflow.com/questions/3552303/how-can-i-make-a-url-link-in-django-that-will-go-to-the-referring-view
    """

    url = request.META.get('REFERER', default)
    parsed = urlparse(url)
    try:
        urlresolvers.resolve(parsed.path)
    except urlresolvers.Resolver404:
        back_url = default
    else:
        back_url = url

    return back_url



@login_required
def like_ajax(request, content_type_id, object_id):
    """
    A view for generating likes via AJAX.
    """ 

    # generate the like for the object
    like(request, content_type_id, object_id)

    # return an AJAX response
    return HttpResponse(json.dumps({'success': True}), mimetype='application/javascript')



@login_required
def like_noajax(request, content_type_id, object_id):
    """
    A view for generating likes via normal HTTP request which
    automatically redirects the user back to the referring URL if
    the referer is on this server, otherwise to the settings.DEFAULT_LIKE_BACK_URL.
    """ 

    # generate the like for the object
    like(request, content_type_id, object_id)

    return HttpResponseRedirect(generate_back_url(request))



@login_required
def like_autodetect(request, content_type_id, object_id):
    """
    Default like view - automatically detects if the request is
    via AJAX or not and returns the appropriate view.
    """

    if request.is_ajax():
        return like_ajax(request, content_type_id, object_id)
    else:
        return like_noajax(request, content_type_id, object_id)



def get_like_view_params(obj):
    """
    A shortcut for returning the content type ID and object ID
    for the given object, which can be passed to one of the like views.
    """

    ct = ContentType.objects.get_for_model(obj.__class__)
    return ct.pk, obj.pk

