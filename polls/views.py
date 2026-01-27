from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from . import models, forms


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


def create_poll(request):
    """Show form to create a new poll."""
    context = {"form": forms.PollForm()}
    return render(request, "polls/create_poll.html", context)


def create_poll_submit(request):
    """Handle form to create a new poll."""
    form = forms.PollForm(request.POST)
    if not form.is_valid():
        return render(request, "polls/create_poll.html", {"form": form})
    poll = form.save()
    return redirect("polls:create_question", poll_id=poll.id)


def edit_poll(request, poll_id: int):
    """Show form to edit a poll."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    form = forms.PollForm(instance=poll)
    context = {"poll": poll, "form": form}
    return render(request, "polls/edit_poll.html", context)


def edit_poll_submit(request, poll_id: int):
    """Handle form to edit a poll."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    form = forms.PollForm(request.POST, instance=poll)
    if not form.is_valid():
        context = {"poll": poll, "form": form}
        return render(request, "polls/edit_poll.html", context)
    form.save()
    return redirect("polls:entry", poll_id=poll_id)


def delete_poll(request, poll_id: int):
    """Show form to edit a poll."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    poll.delete()
    return redirect("polls:index")


def questions(request, poll_id: int):
    """List all questions for a poll."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    return render(request, "polls/questions.html", {"poll": poll})


def create_question(request, poll_id: int):
    """Show form to create a question."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    form = forms.QuestionForm()
    choice_formset = forms.CreateChoiceFormSet()
    context = {"poll": poll, "form": form, "choice_formset": choice_formset}
    return render(request, "polls/create_question.html", context)


def create_question_submit(request, poll_id: int):
    """Handle form to create a question."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    form = forms.QuestionForm(request.POST)
    choice_formset = forms.CreateChoiceFormSet(request.POST)
    if not form.is_valid() or not choice_formset.is_valid():
        context = {"poll": poll, "form": form, "choice_formset": choice_formset}
        return render(request, "polls/create_question.html", context)
    question = form.save(commit=False)
    question.poll = poll
    question.save()
    choices = choice_formset.save(commit=False)
    for choice in choices:
        choice.question = question
        choice.save()
    return redirect("polls:create_question", poll_id=poll_id)


def create_question_add_choice(request, poll_id: int):
    """Add a choice to the form to create a question."""
    form_data = request.POST.copy()
    choice_count = int(form_data["choice_set-TOTAL_FORMS"])
    form_data["choice_set-TOTAL_FORMS"] = str(choice_count + 1)
    poll = get_object_or_404(models.Poll, pk=poll_id)
    form = forms.QuestionForm(request.POST)
    choice_formset = forms.CreateChoiceFormSet(form_data)
    context = {"poll": poll, "form": form, "choice_formset": choice_formset}
    return render(request, "polls/create_question.html", context)


def edit_question(request, poll_id: int, question_id: int):
    """Show form to edit a question."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    question = get_object_or_404(models.Question, pk=question_id)
    form = forms.QuestionForm(instance=question)
    choice_formset = forms.EditChoiceFormSet(instance=question)
    context = {
        "poll": poll,
        "question": question,
        "form": form,
        "choice_formset": choice_formset,
    }
    return render(request, "polls/edit_question.html", context)


def edit_question_submit(request, poll_id: int, question_id: int):
    """Handle form to edit a question."""
    poll = get_object_or_404(models.Poll, pk=poll_id)
    question = get_object_or_404(models.Question, pk=question_id)
    form = forms.QuestionForm(request.POST, instance=question)
    choice_formset = forms.EditChoiceFormSet(request.POST, instance=question)
    if not form.is_valid() or not choice_formset.is_valid():
        context = {
            "poll": poll,
            "question": question,
            "form": form,
            "choice_formset": choice_formset,
        }
        return render(request, "polls/edit_question.html", context)
    form.save()
    choice_formset.save()
    return redirect("polls:questions", poll_id=poll_id)


def edit_question_add_choice(request, poll_id: int, question_id: int):
    """Add a choice to the form to edit a question."""
    form_data = request.POST.copy()
    choice_count = int(form_data["choice_set-TOTAL_FORMS"])
    form_data["choice_set-TOTAL_FORMS"] = str(choice_count + 1)
    form = forms.QuestionForm(request.POST)
    question = get_object_or_404(models.Question, pk=question_id)
    choice_formset = forms.CreateChoiceFormSet(form_data, instance=question)
    poll = get_object_or_404(models.Poll, pk=poll_id)
    context = {
        "poll": poll,
        "question": question,
        "form": form,
        "choice_formset": choice_formset,
    }
    return render(request, "polls/edit_question.html", context)


def delete_question(request, poll_id: int, question_id: int):
    """Delete a question."""
    question = get_object_or_404(models.Question, pk=question_id)
    question.delete()
    return redirect("polls:questions", poll_id=poll_id)


def entry(request, poll_id: int):
    """Show a form to respond to a poll."""
    poll = models.Poll.objects.get(pk=poll_id)
    return render(request, "polls/entry.html", {"poll": poll})


def entry_submit(request, poll_id: int):
    """Handle form to respond to a poll."""
    form_data = request.POST
    poll = get_object_or_404(models.Poll, pk=poll_id)
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
    poll = get_object_or_404(models.Poll, pk=poll_id)
    return render(request, "polls/results.html", {"poll": poll})
