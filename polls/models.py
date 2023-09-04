from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    """The Question class - use for create question by
    adding text (question text) and publish date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """return the question text"""
        return self.question_text

    def was_published_recently(self):
        """to check that the question was published recently or not
        return true if yes. Otherwise, return False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """The Choice model class - use for create the choice for the question
    by adding choice text and votes.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """return the choice text"""
        return self.choice_text
