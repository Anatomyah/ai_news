from .models import *
from django import forms
from django.contrib.contenttypes.models import ContentType


class ArticleForm(forms.ModelForm):
    """
    ModelForm for creating and updating articles.

    The form is based on the Article model and includes all fields of the model.
    Additional widgets and custom settings are applied for specific fields.

    Attributes:
        Meta: Defines the form's configuration, including the model, fields, widgets, labels, and error messages.
    """
    # Meta class definition with model, fields, widgets, labels, and error messages
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'body': forms.Textarea(attrs={'maxlength': '500'})
        }

    labels = {
        'field': 'field label'
    }

    error_messages = {
        'validator': 'error message'
    }


class PermissionRequestForm(forms.Form):
    """
    Form for requesting permissions related to the Article model.

    The form includes a multiple choice field for selecting permissions,
    which are filtered to be relevant to the Article model.

    Attributes:
        content_type: Retrieves the ContentType for the 'article' model.
        permissions (ModelMultipleChoiceField): Field for selecting multiple permissions with a checkbox interface.
    """
    # Fields definition
    content_type = ContentType.objects.get(model='article')
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type=content_type),
        widget=forms.CheckboxSelectMultiple,
        label="Permissions"
    )