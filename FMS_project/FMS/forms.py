from django import forms
from models import User, UserProfile, Supervisor, Student, Project

class UserForm(forms.ModelForm):	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
		model = UserProfile
		fields = ('picture', 'about_me', 'website', 'topic_choices')

class SupervisorForm(forms.ModelForm):
	class Meta:
		model = Supervisor
		fields = ('job_title',)

class StudentProfileForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('degree', 'major', 'advisor', 'advisor_email')
		
class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('title', 'description', 'level', 'project_topic')

class SearchForm(forms.Form):
    search = forms.CharField()

