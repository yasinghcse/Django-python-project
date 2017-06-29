from django import forms
from myapp.models import Topic, Student, PageHitCount

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

#student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        #fields=['username','password','first_name','last_name','address', 'city','province','age','date_joined','is_active','email']
        fields = ['username', 'password', 'first_name', 'last_name', 'address', 'city', 'province', 'age', 'date_joined', 'is_active', 'email', 'stud_pic']


#counter form -- not currently in use
class PageHitCountForm(forms.ModelForm):
    class Meta:
        model= PageHitCount
        fields = ['count']

class ForgetPwdForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)
