from django import forms
from django.contrib.auth.models import User

class UbahPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password",)
        widgets ={
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),

        }

class UserUbahPasswordForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserUbahPasswordForm, self).__init__(*args, **kwargs)

    def clean_password_lama(self):
        password = self.cleaned_data.get('password_lama')
        if not self.user.check_password(password):
            raise forms.ValidationError("Password salah!")
        return password
    def clean(self):
        cleaned_data = super(UserUbahPasswordForm,self).clean()
        baru = self.cleaned_data.get('password_baru')
        ulangi = self.cleaned_data.get('ulangi_password')
        if not baru == ulangi:
            raise forms.ValidationError("Password baru dan Ulangi password tidak cocok!")
        return cleaned_data

    password_lama = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    password_baru = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    ulangi_password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))