import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question class
       Attributes:

           question_text: string
           pub_date: datetime
           end_date: datetime

       Methods:
           was_published_recently (bool): show question was published recently.
           is_published (bool): show question is published or not.
           can_vote (bool): show question can vote or not.
       """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)

    def __str__(self):
        """Returns a string representation of this Question"""
        return self.question_text

    def was_published_recently(self):
        """Returns True if this Question was published recently"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Returns True if this Question is published"""
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """Returns True if this Question can vote"""
        if self.end_date is None:
            return self.pub_date < timezone.now()
        return self.pub_date <= timezone.now() <= self.end_date


class Choice(models.Model):
    """Choice class
        Attributes:
            question (Question): Question class that want this choice there.
            choice_text (str): Text of the choice.
            votes (int): Number of votes in this question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Returns a string representation of this Choice"""
        return self.choice_text

