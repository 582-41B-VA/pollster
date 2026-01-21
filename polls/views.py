from django.shortcuts import render
from django.utils import timezone
from .forms import IndexForm
from . import models


def index(request):
    """List all polls."""
    form = IndexForm(request.GET)
    if not form.is_valid():
        form = IndexForm()
    default_sort_order = IndexForm.SORT_ORDERS[0][0]
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


def results(request, poll_id: int):
    """Show results for a poll."""
    poll = Poll.objects.get(pk=poll_id)
    return render(request, "polls/results.html", {"poll": poll})
