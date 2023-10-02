from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField (auto_now=True)
    otp=models.SmallIntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)   
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    auth_token = models.CharField(max_length=100,default="")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path) 

        if img.height > 300 or img.width > 300:  
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
