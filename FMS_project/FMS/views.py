from django.db.models import Q
import re
from django.shortcuts import render
from django.http import HttpResponse
from FMS_project import settings
from models import User, UserProfile, Supervisor, Student, Topic
from forms import UserForm

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

def profile_form(request):
    if request.user.is_authenticated():
        form = UserForm()
        return render(request, 'FMS/profile_form.html',{'form':form})
    else:
        return HttpResponse("You are not logged in.")


#profile page
def profile(request, user_name_slug):
    context_dict = {}

    try:
        profile = UserProfile.objects.get(slug=user_name_slug)
        topics = profile.topic_choices.all()
        user = profile.user

        if not user.email.find('student') == -1:
            details = Student.objects.filter(user_profile=profile)[0]
            is_supervisor = False
        else:
            details = Supervisor.objects.filter(user_profile=profile)[0]
            is_supervisor = True

        context_dict = {'user': user, 'profile': profile, 'topics': topics, 'details': details, 'is_supervisor': is_supervisor}


    except UserProfile.DoesNotExist:
        pass
    return render(request, 'FMS/profile.html', context_dict)

'''def favorite_supervisor(request):
    if request.user.is_authenticated():
        user = request.user
        if not user.email.find('student') == -1:
            profile = UserProfile.objects.filter(user=user)
    else:
        return HttpResponse("You are not logged in.")'''



# views.py
def search(request):
    user = request.user
    output = ' '
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
            outputHTML =['']
            print len(found_entries)
            if len(found_entries) > 0:
                outputList = {}
                i=0

                mail = str(user.email).lower()
                if mail.find('student') != -1:
                    for entry in found_entries:
                        if i == 0:
                            returned_users = Supervisor.objects.filter(user_profile__topic_choices=entry)
                            found_users = returned_users
                            es_count = [len(found_users)]
                            print es_count[i]

                        else:
                            returned_users = Supervisor.objects.filter(user_profile__topic_choices=entry)
                            found_users = found_users | returned_users
                            es_count.append(len(returned_users))
                            print es_count[i]
                        print entry
                        if es_count[i] != 0:
                            outputHTML.append('<div class="jumbotron"> <h2>'+str(entry)+'</h2> \n')
                            for x in returned_users:
                                outputHTML.append(' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title">'
                                                  + str(x.user_profile.user.first_name) + ' ' + str(x.user_profile.user.last_name) + '</h3> </div><div class="panel-body"> ' #HEADER
                                                  )
                                outputHTML.append('  <a class="pull-left" href="#"> <div class="well well-sm"> <img class="media-object" src=" '+str(settings.MEDIA_URL) + "profile_images/avatar.jpg" +' "/></div></a>')
                                outputHTML.append('<dl>')
                                try:
                                    if str(x.user_profile.user.email) != '':
                                        outputHTML.append('<dt>' + str(x.user_profile.user.email) + '</dt>')
                                except:
                                    print 'email not supplied'
                                try:
                                    if str(x.user_profile.website) != '':
                                        outputHTML.append('<dt>' +str(x.user_profile.website) + '</dt>')
                                except:
                                    print 'website not supplied'
                                try:
                                    z=0
                                    length = len(x.user_profile.topic_choices.all())
                                    for each in x.user_profile.topic_choices.all():
                                        outputHTML.append('<dt>')
                                        if z != length-1:
                                            outputHTML.append(each.name + ', ')
                                        else:
                                            outputHTML.append(each.name + '</dt>')
                                        z+= 1
                                except:
                                    print 'topics not supplied'
                                try:
                                    if str(x.user_profile.about_me) != '':
                                        outputHTML.append(str(x.user_profile.about_me))
                                except:
                                    print 'about me not supplied'
                                outputHTML.append('</dl></div><a href="#" class="btn btn-sm btn-success">Favourite <span class="glyphicon glyphicon-star-empty"></span></a></div>')
                            outputHTML.append('</div>')
                            i= i+1
                            output = ''.join(outputHTML)

                else:
                    for entry in found_entries:
                        if i == 0:
                            returned_users = Student.objects.filter(user_profile__topic_choices=entry)
                            found_users = returned_users
                            es_count = [len(found_users)]
                            print es_count[i]

                        else:
                            returned_users = Student.objects.filter(user_profile__topic_choices=entry)
                            found_users = found_users | returned_users
                            es_count.append(len(returned_users))
                            print es_count[i]
                        print entry
                        if es_count[i] != 0:
                            outputHTML.append('<div class="jumbotron"> <h2>'+str(entry)+'</h2> \n')
                            for x in returned_users:
                                outputHTML.append(' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title">'
                                                  + str(x.user_profile.user.first_name) + ' ' + str(x.user_profile.user.last_name) + '</h3> </div><div class="panel-body"> ' #HEADER
                                                  )
                                outputHTML.append('  <a class="pull-left" href="#"> <div class="well well-sm"> <img class="media-object" src=" '+str(settings.MEDIA_URL) + "profile_images/avatar.jpg" +' "/></div></a>')
                                outputHTML.append('<dl>')
                                try:
                                    if str(x.user_profile.email) != '':
                                        outputHTML.append('<dt>' + str(x.user_profile.user.email) + '</dt>')
                                except:
                                    print 'email not supplied'
                                try:
                                    if str(x.user_profile.website) != '':
                                        outputHTML.append('<dt>' +str(x.user_profile.website) + '</dt>')
                                except:
                                    print 'website not supplied'
                                try:
                                    z=0
                                    length = len(x.user_profile.topic_choices.all())
                                    for each in x.user_profile.topic_choices.all():
                                        outputHTML.append('<dt>')
                                        if z != length-1:
                                            outputHTML.append(each.name + ', ')
                                        else:
                                            outputHTML.append(each.name + '</dt>')
                                        z+= 1
                                except:
                                    print 'topics not supplied'
                                try:
                                    if str(x.user_profile.about_me) != '':
                                        outputHTML.append(str(x.user_profile.about_me))
                                except:
                                    print 'about me not supplied'
                                outputHTML.append('</dl></div><a href="#" class="btn btn-sm btn-success">Favourite <span class="glyphicon glyphicon-star-empty"></span></a></div>')
                            outputHTML.append('</div>')
                            i= i+1
                            output = ''.join(outputHTML)
                print output
                return render(request, 'FMS/search.html', {'found_entries':found_entries, 'outputHTML':output })
            else:
                print "OI"
                fields = ['first_name', 'last_name'] # your field names
                query = None
                for term in terms:
                    for field in fields:
                        qry = Q(**{'%s__icontains' % field: term})
                        if query is None:
                            query = qry
                        else:
                            query = query | qry
                returned_users = User.objects.filter(query)

                outputHTML.append('<div class="jumbotron"> <h2> Users </h2> \n')
                for x in returned_users:
                    profile = UserProfile.objects.filter(user=x)[0]
                    outputHTML.append(
                        ' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title">'
                        + str(x.first_name) + ' ' + str(
                            x.last_name) + '</h3> </div><div class="panel-body"> '
                        # HEADER
                        )
                    outputHTML.append(
                        '  <a class="pull-left" href="#"> <div class="well well-sm"> <img class="media-object" src=" ' + str(
                            settings.MEDIA_URL) + "profile_images/avatar.jpg" + ' "/></div></a>')
                    outputHTML.append('<dl>')
                    try:
                        if str(x.email) != '':
                            outputHTML.append('<dt>' + str(x.email) + '</dt>')
                    except:
                        print 'email not supplied'
                    try:
                        if str(profile.website) != '':
                            outputHTML.append('<dt>' + str(profile.website) + '</dt>')
                    except:
                        print 'website not supplied'
                    try:
                        z = 0
                        length = len(profile.topic_choices.all())
                        for each in profile.topic_choices.all():
                            outputHTML.append('<dt>')
                            if z != length - 1:
                                outputHTML.append(each.name + ', ')
                            else:
                                outputHTML.append(each.name + '</dt>')
                            z += 1
                    except:
                        print 'topics not supplied'
                    try:
                        if str(profile.about_me) != '':
                            outputHTML.append(str(profile.about_me))
                    except:
                        print 'about me not supplied'
                    outputHTML.append('</dl></div><a href="#" class="btn btn-sm btn-success">Favourite <span class="glyphicon glyphicon-star-empty"></span></a></div>')
                outputHTML.append('</div>')

                output = ''.join(outputHTML)
                print output
                for each in returned_users:
                    print each
                return render(request, 'FMS/search.html', {'found_entries':returned_users, 'outputHTML':output })
    else:
        form = SearchForm()
        return render(request, 'FMS/search.html', {'form':form})


'''#do we need separate view for edited version
def project(request):

def search(request):'''