from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from datetimepicker.widgets import DateTimePicker
from .models import Member, Internship, InternApplication, OrgUnit, InternshipTask, InternshipTaskQuestion, \
    InternshipTaskAnswer, InternshipTaskProgress, InternshipTaskEndAnswers, Resources, InternshipFocus, \
    InternshipFocusEndAnswers, PerformanceFeedback, PerformanceFeedbackAnswers


class InternApplicationForm(forms.ModelForm):
    class Meta:
        model = InternApplication
        fields = ('internship', 'applicant', 'letter', 'notes', 'state')
        labels = {
            'letter': _('Application Letter'),
        }
        help_texts = {
            'letter': _('Tell the internship supervisor why they should select you.'),
        }
        error_messages = {
            'letter': {
                'max_length': _("This application letter is too long."),
            },
        }


class InternshipForm(forms.ModelForm):
    """
    Creating a new Internsip
    """

    class Meta:
        model = Internship
        fields = (
            'company', 'title', 'description', 'registration_start_date', 'registration_end_date', 'start_date',
            'end_date', 'openings'
        )
        widgets = {
            'registration_start_date': DateTimePicker(options={"format": "%Y-%m-%d %H:%M", }),
            'registration_end_date': DateTimePicker(options={"format": "%Y-%m-%d %H:%M", }),
            'start_date': DateTimePicker(options={"format": "%Y-%m-%d %H:%M", }),
            'end_date': DateTimePicker(options={"format": "%Y-%m-%d %H:%M", }),
        }


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserFormCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('bio', 'phone', 'street', 'street2', 'city', 'state', 'zip', 'country')


class OrgNewForm(forms.ModelForm):
    class Meta:
        model = OrgUnit
        fields = (
            'org_name', 'org_type', 'street', 'street2', 'city',
            'state', 'zip', 'country', 'industry', 'bio', 'logo', 'website'
        )


class TaskNewForm(forms.ModelForm):
    class Meta:
        model = InternshipTask
        fields = (
            'name', 'details', 'estimation'
        )


class TaskNewQuestionForm(forms.ModelForm):
    class Meta:
        model = InternshipTaskQuestion
        fields = (
            'question',
        )


class TaskAnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = InternshipTaskAnswer
        fields = (
            'answer',
        )


class TaskProgressForm(forms.ModelForm):
    class Meta:
        model = InternshipTaskProgress
        fields = (
            'progress',
        )


class InternshipTaskEndAnswersForm(forms.ModelForm):
    class Meta:
        model = InternshipTaskEndAnswers
        fields = (
            'text',
    )
    
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('extra')
        super(InternshipTaskEndAnswersForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.fields['answer_%d' % question.id] = forms.IntegerField(label=question, max_value=10, min_value=0)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)


class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resources
        fields = (
            'type', 'url', 'text', 'social',
        )


class FocusNewForm(forms.ModelForm):
    class Meta:
        model = InternshipFocus
        fields = (
            'internship', 'length', 'text',
        )


class InternshipFocusEndAnswersForm(forms.ModelForm):
    class Meta:
        model = InternshipFocusEndAnswers
        fields = (
            'answer',
        )


class PerformanceFeedbackNewForm(forms.ModelForm):
    class Meta:
        model = PerformanceFeedback
        fields = (
                  'internship', 'question',
                  )


class PerformanceFeedbackAnswersForm(forms.ModelForm):
    class Meta:
        model = PerformanceFeedbackAnswers
        fields = (
                  'answer',
                  )

class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, help_text='100 characters max')
    email = forms.EmailField(required=True)
    comment = forms.CharField(required=True, widget=forms.Textarea)

