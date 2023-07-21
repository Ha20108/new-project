from django import forms
from .models import Router



class LoginForm(forms.ModelForm):

    host = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Host'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device name'}), required=True)
    class Meta:
        model = Router
        fields = ['host', 'username', 'password','name']

class HotspotForm(forms.Form):
    image = forms.ImageField()
    num_users = forms.IntegerField(min_value=1, max_value=2000)
    num_images_per_page = forms.IntegerField(min_value=1, max_value=60)
    num_columns = forms.IntegerField(min_value=1, max_value=3)
    font_size = forms.IntegerField(min_value=12, max_value=24)
    text_x = forms.IntegerField()
    text_y = forms.IntegerField()
    uptime = forms.IntegerField()
    total_limit = forms.IntegerField()

    num_digits = forms.IntegerField(min_value=4, max_value=12)
    profile = forms.ChoiceField(label='ملف السرعه', choices=[])

    def __init__(self, *args, **kwargs):
        profile_choices = kwargs.pop('choices', None)
        super().__init__(*args, **kwargs)
        if profile_choices:
            self.fields['profile'].choices = profile_choices

