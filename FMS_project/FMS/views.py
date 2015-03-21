from django.shortcuts import render
from django.http import HttpResponse
from FMS.models import User, UserProfile, Supervisor, Student

def index(request):

    if request.user.is_authenticated():
        # Construct a dictionary to pass to the template engine as its context.
        # Note the key boldmessage is the same as {{ boldmessage }} in the template!
        #context_dict = {'boldmessage': "Hello World!"}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.

        return render(request, 'FMS/index.html')
    else:
        return HttpResponse("You are not logged in.")

#do we need separate view for edited version
def my_profile(request):
    if request.user.is_authenticated():
        user = request.user
        userObj = User.objects.get(username=user.username)
        profile = UserProfile.objects.filter(user=userObj)[0]
        
        if not userObj.email.find('student'):
            details = Student.objects.filter(user_profile=profile)[0]

        else:
            details = Supervisor.objects.filter(user_profile=profile)[0]


        context_dict = {'user': userObj, 'profile': profile, 'details': details}

        return render(request, 'FMS/profile.html', context_dict)
    else:
        return HttpResponse("You are not logged in.")

'''#do we need separate view for edited version
def project(request):

def search(request):'''