import django.forms as forms

class SearchForm(forms.Form):
    dept = forms.CharField(max_length = 10)
    c_num = forms.CharField(max_length = 4)
    c_code = forms.CharField(max_length = 5)

class RemoveForm(forms.Form):
    index = forms.IntegerField()