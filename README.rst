django-likeable
===============

Adds "liking" functionality which aims to be scale-friendly
(see `django-nonrel <http://www.allbuttonspressed.com/projects/django-nonrel>`_).
Note that this app is not yet tested at scale, but will be at some point in the
near future.

In the meantime, it simply adds "liking" functionality to your models.

Quick Installation
------------------
1. Add the ``django-likeable`` app to your Python path.
2. Add ``likeable`` to your list of ``INSTALLED_APPS`` in your project settings.
3. Create your likeable model:

::

    from likeable import Likeable
    from django.contrib.auth.models import User

    class BlogEntry(Likeable):

        author = models.ForeignKey(User)
        content = models.TextField()
        created = models.DateTimeField(auto_now_add=True)

    class BlogEntryComment(Likeable):
        
        entry = models.ForeignKey(BlogEntry)
        author = models.ForeignKey(User)
        content = models.TextField()
        created = models.DateTimeField(auto_now_add=True)

Liking Content Manually
-----------------------
You can use the provided ``Likeable.like`` function to automatically like a particular
object by a given user, such as:

::

    from likeable import Like
    from models import BlogEntry, BlogEntryComment
    from django.contrib.auth.models import User

    ...

    # harry posts a blog entry
    harry = User.objects.create(username='harry')
    blog_entry = BlogEntry.objects.create(author=harry, content="This is my first post.")

    ...

    # sally likes the blog entry
    sally = User.objects.create(username='sally')
    blog_entry.like(sally)

Liking Content Via Provided Views
---------------------------------
Make sure your project's ``urls.py`` file looks something like this:

::

    from django.conf.urls.defaults import patterns, include, url

    urlpatterns = patterns('',

        # ...

        # add django-likeable's urls
        url(r'^like/', include('likeable.urls')),

        # ...
    )

**Enabled URLs**

``like/<content_type_id>/<object_id>``

Auto-detects whether a request comes in via
a plain GET request or an AJAX request, and handles it according to the following two
views.

``like/noajax/<content_type_id>/<object_id>``

Attempts to like the object whose
content type ID is ``<content_type_id>`` and primary key is ``<object_id>`` (both
positive integers). This function automatically attempts to redirect the user to the
referring URL after liking the given object. If no object matching the given criteria is
found, an HTTP 404 error will be generated.

``like/ajax/<content_type_id>/<object_id>``

Attempts to like the object whose
content type ID is ``<content_type_id>`` and primary key is ``<object_id>`` (both
positive integers). This function returns a JSON object of the format
``{'success': true}`` upon success. If no object matching the given criteria is
found, an HTTP 404 error will be generated.

