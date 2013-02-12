from django import forms
from vault.models import CredentialGroup, Credential

class CredentialGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CredentialGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
    class Meta:
        model = CredentialGroup
        fields = ('name', 'description')

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
