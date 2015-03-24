from django import forms
from models import User, UserProfile, Supervisor, Student, Project

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required= True)
    last_name = forms.CharField(max_length=30, required= True)
    email = forms.EmailField(max_length=254, required= True)

    class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    website = forms.URLField(required=False)
    #school_ID = forms.ModelChoiceField()
    #picture = forms.ImageField(upload_to='profile_images', required=False)
    about_me = forms.CharField(max_length=500, required=False)
    #topic_choices = forms.ModelMultipleChoiceField()
    class Meta:
		model = UserProfile
		fields = ('website', 'school_ID', 'picture', 'about_me', 'topic_choices')

class SupervisorForm(forms.ModelForm):
    job_title = forms.CharField(max_length=128, required=False)
    availability = forms.BooleanField()
    class Meta:
		model = Supervisor
		fields = ('job_title','availability')

class StudentForm(forms.ModelForm):
    degree= forms.CharField(max_length = 128, required=False)
    major= forms.CharField(max_length = 128, required=False)
    advisor= forms.CharField(max_length = 128, required=False)
    advisor_email= forms.EmailField(max_length=254, required= False)

    class Meta:
		model = Student
		fields = ('degree', 'major', 'advisor', 'advisor_email')
		
class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('title', 'description', 'level', 'project_topic')

class SearchForm(forms.Form):
    search = forms.CharField()

