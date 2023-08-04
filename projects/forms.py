from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        labels = {
            'title': 'Название',
            'featured_image': 'Изображение',
            'description': 'Описание',
            'demo_link': 'Ссылка на демо',
            'source_link': 'Ссылка на код',
            'tags': 'Теги'
        }

        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})

        # self.fields['title'].widget.attrs.update({'class': 'input input--text', 'placeholder': 'Add title'})
        # self.fields['description'].widget.attrs.update({'class': 'input input--text', 'placeholder': 'Add text'})
        # self.fields['tags'].widget.attrs.update({'class': 'taggggs' })


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Ваш выбор',
            'body': 'Добавьте комментарий'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
