from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_future_question(self):
        """is_published() return False if the current date is before the question's publication date"""
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_past_question(self):
        """is_published() return True if the current date is after the question's publication date"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_recent_question(self):
        """is_published() return True if the current date is the same as the question's publication date."""
        time = timezone.now()
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_end_date_is_none(self):
        """can_vote() returns True if end date is None."""
        time = timezone.localtime()
        question = Question(pub_date=time)
        self.assertIsNone(question.end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_is_pub_date(self):
        """can_vote() returns True if current date is question's publication date."""
        recent_time = timezone.localtime()
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_before_end_date(self):
        """can_vote() returns True if current date is before the end date of the question."""
        before_time = timezone.localtime() - datetime.timedelta(hours=46, minutes=59)
        end_time = timezone.localtime() + datetime.timedelta(hours=46, minutes=59)
        question = Question(pub_date=before_time, end_date=end_time)
        self.assertIs(question.can_vote(), True)

    def test_cannot_vote_after_end_date(self):
        """can_vote() returns False if current date is after the end date of the question."""
        time = timezone.localtime()
        end_time = timezone.localtime() - datetime.timedelta(hours=46, minutes=59)
        question = Question(pub_date=time, end_date=end_time)
        self.assertIs(question.can_vote(), False)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)