from django.shortcuts import render, redirect
from django.utils import timezone
from . import forms
from . import models


def index(request):
    """List all polls."""
    form = forms.IndexForm(request.GET)
    if not form.is_valid():
        form = forms.IndexForm()
    default_sort_order = forms.IndexForm.SORT_ORDERS[0][0]
    sort_order = form.cleaned_data["sort_order"] or default_sort_order
    polls = (
        models.Poll.objects.published()
        .search(form.cleaned_data["search"])
        .order_by(sort_order)
    )
    return render(request, "polls/index.html", {"polls": polls, "form": form})


def entry(request, poll_id: int):
    """Show a form to respond to a poll."""
    poll = models.Poll.objects.get(pk=poll_id)
    return render(request, "polls/entry.html", {"poll": poll})


def entry_submit(request, poll_id: int):
    """Handle form to respond to a poll."""
    form_data = request.POST
    poll = models.Poll.objects.get(pk=poll_id)
    entry = models.Entry(poll=poll, date=timezone.now())
    entry.save()
    for question in poll.question_set.all():
        # question and choice ids in form data are strings
        selected_choice_id = int(form_data[str(question.id)])
        selected_choice = models.Choice.objects.get(pk=selected_choice_id)
        answer = models.Answer(entry=entry, choice=selected_choice)
        answer.save()
    return redirect("polls:results", poll_id=poll_id)


def results(request, poll_id: int):
    """Show results for a poll."""
    poll = models.Poll.objects.get(pk=poll_id)
    return render(request, "polls/results.html", {"poll": poll})


def create_poll(request):
    """Show a form to create a poll."""
    form = forms.PollForm()
    return render(request, "polls/create_poll.html", {"form": form})


def create_poll_submit(request):
    """Handle form to create a poll."""
    form = forms.PollForm(request.POST)
    if not form.is_valid():
        return render(request, "polls/create_poll.html", {"form": form})
    poll = form.save()
    return redirect("polls:index")
