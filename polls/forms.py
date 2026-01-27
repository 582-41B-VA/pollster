from django import forms
from . import models

from . import models


class IndexForm(forms.Form):
    SORT_ORDERS = [
        ("-pub_date", "Date: new to old"),
        ("pub_date", "Date: old to new"),
        ("title", "Title: A to Z"),
        ("-title", "Title: Z to A"),
    ]

    search = forms.CharField(required=False)
    sort_order = forms.ChoiceField(
        label="Sort", required=False, choices=SORT_ORDERS
    )


class PollForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = ["title", "description", "pub_date"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ["text", "order"]
        labels = {"text": "Question"}


EditChoiceFormSet = forms.inlineformset_factory(
    parent_model=models.Question,
    model=models.Choice,
    fields=["text"],
    extra=0,
)

CreateChoiceFormSet = forms.inlineformset_factory(
    parent_model=models.Question,
    model=models.Choice,
    fields=["text"],
    extra=2,
)
