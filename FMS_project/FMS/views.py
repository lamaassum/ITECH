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
    user = request.user
    user = User.getObjects(username=user.username)
    profile = UserProfile.getObjects(user=user)

    if user.email.find('student'):
        details = Student.getObjects(user_profile=profile)
    else:
        details = Supervisor.getObjects(user_profile=profile)

    context_dict = {'user': user, 'profile': profile, 'details': details}

    return render(request, 'FMS/profile.html', context_dict)

'''#do we need separate view for edited version
def project(request):

def search(request):'''