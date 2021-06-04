from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    position=models.ForeignKey('Position',on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    bio = models.TextField(max_length=500)
    address= models.CharField(max_length=20)
    total_vote = models.IntegerField(default=0, editable=False)
    image = models.ImageField(verbose_name="Candidate Pic", upload_to='candidate_images/',default='default.jpg')

    def __str__(self):
        return "{} - {}".format(self.name, self.position)

class ControlVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.position, self.status)

