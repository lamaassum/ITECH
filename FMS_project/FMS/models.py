from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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
    about_me = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True, null=True)
    picture =models.ImageField(upload_to='profile_images',blank=True)
    school_ID = models.ForeignKey(School, null=True, blank=True)
    topic_choices = models.ManyToManyField(Topic)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name+" "+self.user.last_name+" "+str(self.user.id))
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


		
class Supervisor(models.Model):
	user_profile = models.OneToOneField(UserProfile,unique=True)
	job_title = models.CharField(max_length=128, blank=True)
	availability= models.BooleanField(default=True)
	def __unicode__(self):
			return self.user_profile.user.username
			
class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    level = models.CharField(max_length=128, blank=True)
    supervisor = models.ForeignKey(Supervisor)
    projectAssigned = models.BooleanField(default=False)
    project_topic = models.ManyToManyField(Topic)

    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title+" "+str(self.id))
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
		
class Student (models.Model):
	user_profile = models.OneToOneField(UserProfile,unique=True)
	degree = models.CharField(max_length = 128, blank=True)
	major = models.CharField(max_length = 128, blank=True)
	advisor = models.CharField(max_length = 128, blank=True)
	advisor_email = models.EmailField(max_length = 254, blank=True, null=True)
	supervisor_choices = models.ManyToManyField(Supervisor,null=True, blank=True)
	project_choices = models.ManyToManyField(Project,null=True, blank=True)
	def __unicode__(self):
		return self.user_profile.user.username
		
class Application(models.Model):
	project = models.ForeignKey(Project)
	student = models.ForeignKey(Student)
	def __unicode__(self):
		return self.project.title +' '+ self.student.user_profile.user.username
