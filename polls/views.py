from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice


class IndexView(generic.ListView):
    """This is IndexView that displays a list of questions.
        Attributes:
            template_name: The name of the template used to render the index.
            context_object_name: The name of the context objects.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """DetailView can displays a question with a choice.
    Attributes:
        model: Question class
        template_name: The name of the template used to render to detail
        model: Question class.
        template_name: The name of the template used to render to detail.
    Methods:
        get_queryset: Get questions by filter.
        get: Redirect to the question page.
    """

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, pk):
        """Excludes any questions that aren't published yet and except error."""
        redirect = HttpResponseRedirect(reverse('polls:index'))
        try:
            self.question = get_object_or_404(Question, pk=pk)
        except IndexError:
            messages.error(request, 'Index not found')
            return redirect
        except Http404:
            messages.error(request, 'Http404 not found')
            return redirect
        if not self.question.can_vote():
            messages.error(request, "This question can't vote")
            return redirect
        return super().get(request, pk=pk)


class ResultsView(generic.DetailView):
    """ResultsView to generate result for each polls.
        Attributes:
            model: Question class.
            template_name: The name of the template used to render to detail.
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """To vote a choice for each question.
        args:
            question_id: Id of this question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def redirect(self):
    """Reidrect to the index page."""
    return HttpResponseRedirect(reverse('polls:index'))
