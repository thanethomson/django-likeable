#
# django-likeable
#
# See LICENSE for licensing details.
#

from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from models import Like, Likeable
from views import get_like_view_params
from django.core.management import call_command

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class Post(Likeable):
    """
    Test class for the Likeable abstract class.
    """

    text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text



class Comment(Likeable):
    """
    Test class for the Likeable abstract class.
    """

    comment = models.CharField(max_length=100)

    def __unicode__(self):
        return self.comment




class LikeableTest(TestCase):
    
    def setUp(self):
        call_command('syncdb', verbosity=0)

        # create a few likeable objects
        self.post1 = Post.objects.create(text="Like me 1!")
        self.post2 = Post.objects.create(text="Like me 2!")
        self.comment1 = Comment.objects.create(comment="Here's a comment.")

        self.post1likes = 0
        self.post2likes = 0
        self.comment1likes = 0

        self.larry = User.objects.create(username='larry')
        self.larry_password = '12345'
        self.larry.set_password(self.larry_password)
        self.larry.save()

        self.harry = User.objects.create(username='harry')
        self.sally = User.objects.create(username='sally')

        # create a few likes
        self.post1.like(self.larry)
        self.post1likes += 1

        self.comment1.like(self.larry)
        self.comment1likes += 1
        
        self.post1.like(self.harry)
        self.post1likes += 1

        self.post1.like(self.sally)
        self.post1likes += 1
        self.comment1.like(self.sally)
        self.comment1likes += 1

        print ""


    def print_like_counts(self):

        print "post1 likes:", self.post1.likes.count()
        print "post2 likes:", self.post2.likes.count()
        print "comment1 likes:", self.comment1.likes.count()
        print ""



    def test_like_counting(self):

        print "Testing simple like counting..."
        #import pdb; pdb.set_trace()

        # check that we can count the likes
        self.assertEqual(self.post1.likes.count(), self.post1likes)
        self.assertEqual(self.post2.likes.count(), self.post2likes)
        self.assertEqual(self.comment1.likes.count(), self.comment1likes)

        self.print_like_counts()



    def test_standard_liking_view(self):
        
        print "Testing plain GET liking..."

        # make sure we log in as larry
        self.client.login(username=self.larry.username, password=self.larry_password)

        # try to generate a like here
        response = self.client.get('/like/%d/%d' % get_like_view_params(self.post2))

        self.assertEqual(self.post2.likes.count(), self.post2likes+1)
        self.assertEqual(response.__class__, HttpResponseRedirect)
        self.print_like_counts()


    
    def test_ajax_liking_view(self):

        print "Testing AJAX liking..."

        # make sure we log in as larry
        self.client.login(username=self.larry.username, password=self.larry_password)

        # try to generate a like here
        response = self.client.get('/like/%d/%d' % get_like_view_params(self.post2),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(self.post2.likes.count(), self.post2likes+1)
        self.assertEqual(response.__getitem__('content-type'), 'application/javascript')
        self.print_like_counts()

        
