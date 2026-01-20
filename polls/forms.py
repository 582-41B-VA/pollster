from django import forms


class IndexForm(forms.Form):
    template_name = "polls/forms/index.html"

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
