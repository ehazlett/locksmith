from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.ModelForm):
    # override the default fields to force them to be required
    # (the django User model doesn't require them)
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
