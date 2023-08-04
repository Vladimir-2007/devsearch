from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skills, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'email': 'Почта',
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  'location', 'bio', 'short_intro', 'profile_image',
                  'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website']
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'username': 'Имя пользователя',
            'location': 'Местонахождение',
            'bio': 'Биография',
            'short_intro': 'Краткое описание',
            'profile_image': 'Изображение',
        }

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input input--text'})


class SkillForm(ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'description': 'Описание'
        }
        exclude = ['owner']  # ? <------------- исключая

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'subject': 'Тема',
            'body': 'Текст'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
