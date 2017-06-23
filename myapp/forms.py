from django import forms
from myapp.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields=['subject', 'intro_course','time','avg_age']
        widgets={'time':forms.RadioSelect}
        labels={'avg_age':'What is your age?','intro_course': 'This should be an introductory level course','time':'Preferred Time'}

class InterestForm(forms.Form):
    interested= forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((0,'No'),(1,'Yes')))
    age = forms.IntegerField(initial=20)
    comments=forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')
