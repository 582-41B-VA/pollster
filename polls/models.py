from typing import Self

from django.db import models
from django.utils import timezone


class PollQuerySet(models.QuerySet):
    def published(self) -> Self:
        return self.filter(pub_date__lt=timezone.now())



    def search(self, query: str) -> Self:
        return self.filter(title__icontains=query)
class Poll(models.Model):
    objects = PollQuerySet.as_manager()

    title = models.CharField()
    description = models.TextField(blank=True)
    pub_date = models.DateField("publication date")

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField()
    order = models.PositiveIntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        ordering = ["order", "text"]

    def __str__(self):
        return self.text


class Choice(models.Model):
    text = models.CharField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def vote_count(self) -> int:
        return self.answer_set.count()

    def __str__(self):
        return self.text


class Entry(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"Entry for {self.poll} on {self.date}"


class Answer(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer for {self.entry}"
