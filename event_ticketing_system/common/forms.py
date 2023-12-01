from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search event by name...',
            },
        )
    )
