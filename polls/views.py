from django.http import HttpResponse

from .models import Poll


def index(request):
    body = "\n".join(
        f"{poll.id} {poll.title}" for poll in Poll.published_polls()
    )
    return HttpResponse(body, content_type="text/plain")


def detail(request, poll_id: int):
    poll = Poll.objects.get(pk=poll_id)
    questions = poll.question_set.all()
    body = f"{poll.title}\n\n"
    for question in questions:
        body += "\t" + question.text + "\n\n"
        choices = question.choice_set.all()
        body += "\n".join(f"\t\t{choice.text}" for choice in choices) + "\n\n"
    return HttpResponse(body, content_type="text/plain")


def results(request, poll_id: int):
    poll = Poll.objects.get(pk=poll_id)
    questions = poll.question_set.all()
    body = f"{poll.title}\n\n"
    for question in questions:
        body += "\t" + question.text + "\n\n"
        choices = question.choice_set.order_by("-votes")
        body += (
            "\n".join(
                f"\t\t{choice.votes}\t{choice.text}" for choice in choices
            )
            + "\n\n"
        )
    return HttpResponse(body, content_type="text/plain")
