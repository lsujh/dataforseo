from django import forms

from countries import COUNTRIES, ENGINE


class SearchForm(forms.Form):
    search_engine = forms.ChoiceField(choices=ENGINE, label="Search engine")
    search_region = forms.ChoiceField(choices=COUNTRIES, label="Search engine location")
    keyword = forms.CharField(widget=forms.TextInput, label="Keyword")

    #
