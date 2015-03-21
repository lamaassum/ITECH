from django.db.models import Q
import re
from django.shortcuts import render
from django.http import HttpResponse
from models import User, UserProfile, Supervisor, Student, Topic
from forms import SearchForm

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
        topics = profile.topic_choices.all()

        if not userObj.email.find('student') == -1:
            details = Student.objects.filter(user_profile=profile)[0]
            is_supervisor = False
        else:
            details = Supervisor.objects.filter(user_profile=profile)[0]
            is_supervisor = True
        context_dict = {'user': userObj, 'profile': profile, 'topics': topics, 'details': details, 'is_supervisor': is_supervisor}
        return render(request, 'FMS/profile.html', context_dict)
    else:
        return HttpResponse("You are not logged in.")


# views.py
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            string = form.cleaned_data['search']
            terms = re.compile(r'[^\s",;.:]+').findall(string)
            fields = ['name', 'id'] # your field names
            query = None
            for term in terms:
                for field in fields:
                    qry = Q(**{'%s__icontains' % field: term})
                    if query is None:
                        query = qry
                    else:
                        query = query | qry
            found_entries = Topic.objects.filter(query).order_by('-name') # your model
            outputList = []
            for entry in found_entries:
                found_supervisors = Supervisor.objects.filter(user_profile__topic_choices=entry)
                print str(entry) + ':' + str(found_supervisors)

            return render(request, 'FMS/search.html', {'found_supervisors':found_supervisors, 'found_entries':found_entries})
    else:
        form = SearchForm()
        return render(request, 'FMS/search.html', {'form':form})


'''#do we need separate view for edited version
def project(request):

def search(request):'''