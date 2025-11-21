from typing import Self

from django.db import models
from django.utils import timezone


class Poll(models.Model):
    title = models.CharField()
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField("publication date")

    @classmethod
    def published_polls(cls) -> list[Self]:
        return [poll for poll in cls.objects.all() if poll.is_published]

    @property
    def is_published(self) -> bool:
        return self.pub_date < timezone.now()

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
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
