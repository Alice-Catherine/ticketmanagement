from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

ALLOWED_EMAIL_DOMAIN = 'company.com'


class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'business_unit', 'password1', 'password2']
        widgets = {
            'business_unit': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_unit'].required = True
        self.fields['business_unit'].empty_label = "Select your Business Unit"
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        domain = email.split('@')[-1].lower() if '@' in email else ''
        if domain != ALLOWED_EMAIL_DOMAIN:
            raise forms.ValidationError(
                f"Registration is only allowed with a @{ALLOWED_EMAIL_DOMAIN} email address."
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'employee'
        if commit:
            user.save()
        return user