from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
    url=models.URLField(unique=True)
    
    
    
    def __str__(self):
        return self.url
    




class Bookmark(models.Model):
    title=models.CharField(max_length=200)
    user=models.ForeignKey(User)
    link=models.ForeignKey(Link)
    
    def get_absolute_url(self):
        return self.link.url
        def __str__(self):
            return '%s , %s ' % (self.user.username , self.link.url)
    
class Tag(models.Model):
    name=models.CharField(max_length=30)
    bookmarks=models.ManyToManyField(Bookmark)

    def __str__(self):
        return self.name

class SharedBookmark(models.Model):
    bookmark=models.ForeignKey(Bookmark,unique=True)
    date=models.DateTimeField(auto_now_add=True)
    votes=models.IntegerField(default=1)
    users_voted=models.ManyToManyField(User)
    
    def __str__(self):
        return "%s ,%s " % (self.bookmark , self.votes)

class Friendship(models.Model):
    #code
    from_friend = models.ForeignKey(User,related_name='friend_set')
    to_friend=models.ForeignKey(User,related_name='to_friend_set')
    invite_status=models.BooleanField(default=False)
    def __str__(self):
        return '%s , %s ' %(self.from_friend,self.to_friend)
    
    class Meta:
        #code
        unique_together=(('from_friend','to_friend'),)
    
    
class Message(models.Model):
    content=models.TextField()
    from_user=models.ForeignKey(User,related_name='from_set')
    to_user=models.ForeignKey(User,related_name='to_set')
    #message_link=models.ForeignKey(Friendship)
    status=models.BooleanField(default=False)
    send_time=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s %s at %s" %(self.message_link.from_friend,self.message_link.to_friend,self.send_time)
    

