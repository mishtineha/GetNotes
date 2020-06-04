
from django.db import models

class Videos(models.Model):
    title = models.CharField(max_length = 30 )
    description = models.TextField(max_length = 300 )
    videofile = models.FileField(upload_to = 'videos/' ,null = True,verbose_name="")
    datetime  = models.DateTimeField(null = False,blank = False,auto_now_add = True )
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    user_viewed = models.IntegerField(default = 0)
    votes = models.IntegerField(default = 0)
    size = models.FloatField(default = 0)
    #liked_user = models.ManyToManyField('auth.User',symmetrical=False,null = True,blank = True)

    def __str__(self):
        return str(self.videofile)
class liked_video(models.Model):
    video = models.ForeignKey('Videos',null = True,blank = True,on_delete = models.CASCADE)
    user = models.ForeignKey('auth.User',null = True,blank = True,on_delete = models.CASCADE)
    
class Viewed_user(models.Model):
    #videoid = models.IntegerField()
    video = models.ForeignKey('Videos',null = True,blank = True,on_delete = models.CASCADE)
    user = models.ForeignKey('auth.User',null = True,blank = True,on_delete = models.CASCADE)
    
class recently_viewed(models.Model):
    videoid = models.IntegerField()
    user = models.ForeignKey('auth.User',null = True,blank = True,on_delete = models.CASCADE)

class Message(models.Model):
    seen = models.BooleanField(default = False)
    to = models.ForeignKey('auth.User',on_delete = models.CASCADE,null = True,blank = True)
    fom = models.CharField(max_length = 30)
    topic = models.CharField(max_length = 30 )
    file = models.CharField(max_length = 30,null = True,blank = True)
   
class Comment(models.Model):
    text = models.CharField(max_length = 300 )
    datetime  = models.DateTimeField(null = False,blank = False,auto_now_add = True )
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    video = models.ForeignKey(Videos,on_delete = models.CASCADE)

class Preferences(models.Model):
    #topic = models.CharField(max_length = 30)
    pref = models.CharField(max_length = 30)
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)

class Notification(models.Model):
    video = models.ForeignKey(Videos,on_delete = models.CASCADE)
    #topic = models.CharField(max_length = 30)
    msg = models.CharField(max_length = 150)
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    seen = models.BooleanField(default = False)

class link(models.Model):
    link = models.CharField(max_length = 1500)
    






