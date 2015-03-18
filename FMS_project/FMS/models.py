from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):  
        return self.name
        
class Topic (models.Model): 
	name = models.CharField(max_length=128)				
	def __unicode__(self):							
		return self.name	
        
class UserProfile (models.Model):
	user = models.OneToOneField(User)
	picture =models.ImageField(upload_to='profile_images',blank=True)
	school_ID = models.ForeignKey(School)
	topic_choices = models.ManyToManyField(Topic)
	def __unicode__(self):
		return self.user.username
		
class Supervisor(models.Model):
	user_profile = models.OneToOneField(UserProfile,unique=True)
	job_title = models.CharField(max_length=128)
	availability= models.BooleanField(default=True)
	def __unicode__(self):
			return self.user_profile.username
			
class Project(models.Model):
	title = models.CharField(max_length=128)
	level = models.CharField(max_length=128)
	supervisor = models.ForeignKey(Supervisor)
	projectAssigned = models.BooleanField(default=False)
	project_topic = models.ManyToManyField(Topic)
	def __unicode__(self):
		return self.title
		
class Student (models.Model):
	user_profile = models.OneToOneField(UserProfile,unique=True)
	degree = models.CharField(max_length = 128)
	major = models.CharField(max_length = 128)
	advisor = models.CharField(max_length = 128)
	advisor_email = models.EmailField(max_length = 254)
	supervisor_choices = models.ManyToManyField(Supervisor,null=True)
	project_choices = models.ManyToManyField(Project,null=True)
	def __unicode__(self):
		return self.user_profile.username
		
class Application(models.Model):
	project = models.ForeignKey(Project)
	student = models.ForeignKey(Student)
	def __unicode__(self):
		return self.project.name +' '+ self.student.username