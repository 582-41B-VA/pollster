from django.http import HttpResponse

from .models import Poll


def index(request):
    """List all polls."""
    body = "\n".join(
        f"{poll.id} {poll.title}" for poll in Poll.objects.published()
    )
    return HttpResponse(body, content_type="text/plain")


def entry(request, poll_id: int):
    """Show a form to respond to a poll."""
    poll = Poll.objects.get(pk=poll_id)
    questions = poll.question_set.all()
    body = f"{poll.title}\n\n"
    for question in questions:
        body += "\t" + question.text + "\n\n"
        choices = question.choice_set.all()
        body += "\n".join(f"\t\t{choice.text}" for choice in choices) + "\n\n"
    return HttpResponse(body, content_type="text/plain")


def results(request, poll_id: int):
    """Show results for a poll."""
    poll = Poll.objects.get(pk=poll_id)
    questions = poll.question_set.all()
    body = f"{poll.title}\n\n"
    for question in questions:
        body += "\t" + question.text + "\n\n"
        choices = question.choice_set.all()
        body += (
            "\n".join(
                f"\t\t{choice.vote_count}\t{choice.text}" for choice in choices
            )
            + "\n\n"
        )
    return HttpResponse(body, content_type="text/plain")
