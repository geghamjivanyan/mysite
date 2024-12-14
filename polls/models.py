import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return "{} | {}".format(self.id, self.question_text) 

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{} | {} - {}".format(self.id, self.choice_text, self.votes)
    

class PollUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    country = models.CharField(max_length=50)

class UserLog(models.Model):
    actions = [
        ('login', "Login Successfully"),
        ('question', "Look question list"),
        ('vote', "Vote a question"),
        ('detail', 'View single question info')
    ]

    user = models.ForeignKey(PollUser, on_delete=models.CASCADE)
    action_time = models.DateTimeField()
    action = models.CharField(choices=actions, max_length=20)
