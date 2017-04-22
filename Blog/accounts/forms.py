from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError("Incorrect username or password.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect username or password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    email2 = forms.EmailField(label="Confirm Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =[
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email!=email2:
            self.add_error("email2", "Emails must match!")
            raise forms.ValidationError("Emails must match!")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            self.add_error("email", "This email has already been used.")
            raise forms.ValidationError("Emails used!")
        return super(UserRegistrationForm, self).clean(*args, **kwargs)