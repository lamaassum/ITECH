from django.core.urlresolvers import reverse
from django.db.models import Q
import re
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from FMS_project import settings
from models import User, UserProfile, Supervisor, Student, Topic, Project
from forms import UserForm, UserProfileForm, StudentForm, SupervisorForm

from forms import SearchForm, AdvancedStudentSearchForm

def index(request):

    user = request.user
    if request.user.is_authenticated():
        isStaff = True
        if str((user.email).lower()).find('student') > -1:
            isStaff = False
        print isStaff
        if isStaff == False:
            users = Supervisor.objects.all()
        else:
            users = Student.objects.all()

        userObj = User.objects.get(username=user.username)
        profile = UserProfile.objects.filter(user=userObj)[0]
        projects = Project.objects.all()
        projectList = []
        topic_choices =  profile.topic_choices.all()
        for each in topic_choices:
            print "TOPIC : " + str(each)
            project_topics = Project.objects.filter(project_topic=each)
            for j in project_topics:
                if str(projectList).find(str(j)) == -1:
                 projectList.append(j)
        a = 0
        projects = Project.objects.none()
        while a < len(projectList):
            print str(a) + ": " + str(projectList[a])
            projects = Project.objects.filter(title=str(projectList[a])) | projects
            a+=1
        projectOutput = ''.join(str(projectList))
        print projectOutput
        projectList = Project.objects.none()
        return render(request, 'FMS/index.html', {'projects':projects[:10], 'users':users[:10]})
    else:
        return HttpResponseRedirect(reverse('login'))


def about(request):
     user = request.user
     if user.is_authenticated():
        return render(request, 'FMS/about.html')
     else:
         return HttpResponseRedirect(reverse('login'))



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
        context_dict = {'user': userObj, 'profile': profile, 'topics': topics, 'details': details, 'is_supervisor': is_supervisor, 'is_mine': True}
        return render(request, 'FMS/profile.html', context_dict)
    else:
        return HttpResponseRedirect(reverse('login'))

def profile_form(request):

    if request.user.is_authenticated():

        user_form = UserForm(prefix="user")
        user_profile_form = UserProfileForm(prefix="profile")
        if not request.user.email.find('student') == -1:
            details_form = StudentForm(prefix="details")
            is_supervisor = False
        else:
            details_form = SupervisorForm(prefix="details")
            is_supervisor= True

        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix="user")
            user_profile_form = UserProfileForm(request.POST, prefix="profile")
            if is_supervisor:
                details_form = SupervisorForm(request.POST, prefix="details")
            else:
                details_form = StudentForm(request.POST, prefix="details")

            if user_form.is_valid() and user_profile_form.is_valid() and details_form.is_valid():
                user_form.save(commit=True)
                user_profile_form.save(commit=True)
                details_form.save(commit=True)
                return render(request, 'FMS/my_profile.html')
            else:
                print user_form.errors
                print user_profile_form.errors
                print details_form.errors

        context_dict = {'user_form':user_form, 'user_profile_form': user_profile_form, 'details_form': details_form}
        return render(request, 'FMS/profile_form.html',context_dict)

    else:
                return HttpResponseRedirect(reverse('login'))


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

        context_dict = {'user': user, 'profile': profile, 'topics': topics, 'details': details, 'is_supervisor': is_supervisor, 'is_mine': False}


    except UserProfile.DoesNotExist:
        pass
    return render(request, 'FMS/profile.html', context_dict)

def profile_form(request):

    if request.user.is_authenticated():


        user = request.user
        userObj = User.objects.get(username=user.username)
        profile = UserProfile.objects.filter(user=userObj)[0]


        if not userObj.email.find('student') == -1:
            details = Student.objects.filter(user_profile=profile)[0]

        else:
            details = Supervisor.objects.filter(user_profile=profile)[0]



        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            user_profile_form = UserProfileForm(request.POST, request.FILES)
            if request.user.email.find('student') == -1:
                details_form = SupervisorForm(data=request.POST)

            else:
                details_form = StudentForm(data=request.POST)


            if user_form.is_valid() and user_profile_form.is_valid() and details_form.is_valid():
                userObj.first_name = request.POST.get('first_name')
                userObj.last_name = request.POST.get('last_name')
                userObj.email = request.POST.get('email')
                userObj.save()


                profile.user = userObj
                profile.about_me = request.POST.get('about_me')
                profile.website = request.POST.get('website')
                profile.schoolID = request.POST.get('schoolID')
                profile.picture = request.POST.get('image_name')
                profile.topic_choices = request.POST.getlist('topic_choices')
                profile.save()

                if userObj.email.find('student') == -1:
                    details.job_title = request.POST.get('job_title')
                    details.profile = profile
                    if(request.POST.get('availability')):
                        details.availability = True;
                    else:
                        details.availability = False;
                else:
                    details.degree = request.POST.get('degree')
                    details.major = request.POST.get('major')
                    details.advisor = request.POST.get('advisor')
                    details.advisor_email = request.POST.get('advisor_email')
                details.save()

                context_dict = {'user': userObj, 'profile': profile, 'topics': profile.topic_choices.all, 'details': details, 'is_mine': True}
                return render(request, 'FMS/profile.html',context_dict)
            '''else:
                print user_form.errors
                print user_profile_form.errors
                print details_form.errors'''

        user_form = UserForm({'first_name':userObj.first_name, 'last_name': userObj.last_name, 'email': userObj.email})
        '''UserForm.first_name = userObj.first_name
        user_form.last_name = userObj.last_name
        user_form.email = userObj.email'''

        user_profile_form = UserProfileForm({'website': profile.website, 'school_ID': profile.school_ID, 'picture': profile.picture,
        'about_me':profile.about_me, 'topic_choices':profile.topic_choices.all()})
        '''user_profile_form.website =profile.website
        #user_profile_form.schoolID =profile.schoolID
        user_profile_form.picture =profile.picture
        user_profile_form.about_me =profile.about_me
        user_profile_form.topic_choices =profile.topic_choices'''

        if not request.user.email.find('student') == -1:
            details_form = StudentForm({'degree': details.degree, 'major': details.major, 'advisor': details.advisor, 'advisor_email': details.advisor_email})

        else:
            details_form = SupervisorForm({'job_title':details.job_title, 'availability': details.availability})


        context_dict = {'user_form':user_form, 'user_profile_form': user_profile_form, 'details_form': details_form}
        return render(request, 'FMS/profile_form.html',context_dict)

    else:
                return HttpResponseRedirect(reverse('login'))

'''def favorite_supervisor(request):
    if request.user.is_authenticated():
        user = request.user
        if not user.email.find('student') == -1:
            profile = UserProfile.objects.filter(user=user)
    else:
                return HttpResponseRedirect(reverse('login')) '''

def issues_search(request, form_class=SearchForm, template_name='advanced_student_search_form.html'):
    if request.user.is_authenticated():
        form = AdvancedStudentSearchForm()
        context = {'searchform':form}
        return render(request, 'FMS/advanced_student_search_form.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def advanced_search(request): #, major, advisor, description, topics
    print "ASDASD"
    user = request.user
    if request.user.is_authenticated():
        isStaff = True
        if str((user.email).lower()).find('student') > -1:
            isStaff = False
        print isStaff
        if isStaff == False:
            users = Supervisor.objects.all()
        else:
            users = Student.objects.all()

        userObj = User.objects.get(username=user.username)
        profile = UserProfile.objects.filter(user=userObj)[0]
    search_results = []
    form = AdvancedStudentSearchForm(request.GET)
    if request.method == 'GET':
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        description = request.GET.get('description')
        topic = request.GET.get('topic')
        operand = request.GET.get('operand')

        terms = []
        fields = []
        if (first_name != ''):
            if (first_name != None):
                terms.append(str(first_name))
                fields.append('user_profile__user__first_name')
        if last_name != '' :
            if last_name != None:
                terms.append(str(last_name))
                fields.append('user_profile__user__last_name')
        if description != '' :
                if description != None:
                    terms.append(str(description))
                    fields.append('user_profile__about_me')

        if isStaff:
            major = request.GET.get('major')
            advisor = request.GET.get('advisor')
            degree = request.GET.get('degree')
            if major != '':
                if major != None:
                    terms.append(str(major))
                    fields.append('major')
            if (advisor != '') :
                if (advisor != None):
                    terms.append(str(advisor))
                    fields.append('advisor')

            if degree != '' :
                if degree != None:
                    terms.append(str(degree))
                    fields.append('degree')
        else:
            job_title = request.GET.get('job_title')
            if job_title != '':
                if job_title != None:
                    terms.append(str(job_title))
                    fields.append('job_title')
            print fields
        print "FIRST NAME: " + str(first_name)
        if form.is_valid():                                #bind data to dict keys

            query = None
            i = 0
            while i < len(terms):
                qry = Q(**{'%s__icontains' % fields[i]: terms[i]})
                if query is None:
                    query = qry
                else:
                    if operand == 'on':
                        query = query | qry
                    else:
                        query = query & qry


                i+=1
            print query
            if query != '' :
                if query != None:
                    found_entries = users.filter(query) # your model
            found_users = ''

            found_topics = ''
            x=0
            if topic != '' :
                if topic != None:
                    terms = re.compile(r'[^\s",;.:]+').findall(topic)
                    for term in terms:
                        field = 'name'

                        qry = Q(**{'%s__icontains' % field: term})
                        found_topics = Topic.objects.filter(qry) # your model
                        print qry
                        for entry in found_topics:
                            if x == 0:
                                try:
                                    found_entries = found_entries.filter(user_profile__topic_choices=entry)
                                except:
                                    found_entries = users.filter(user_profile__topic_choices=entry)

                                found_users = found_entries

                            else:
                                try:
                                    found_entries = found_entries.filter(user_profile__topic_choices=entry)
                                except:
                                    found_entries = users.filter(user_profile__topic_choices=entry)
                                found_users = found_users | found_entries
                            x= x+1
                            print entry
            if found_users == '':
                found_users = found_entries



        print "RESULTS:" +str(found_topics)+str(found_users)
        return render(request, 'FMS/search_results.html', {'found_users':found_users[:50]})
    else:
                return HttpResponseRedirect(reverse('login'))

# views.py
def search(request):
    user = request.user
    if user.is_authenticated():
        output = ' '
        if request.method == 'GET':
            form = SearchForm(request.GET)
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
                                    outputHTML.append(' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title"><a href="/' + str(x.user_profile.slug) +'"> '
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
                                    outputHTML.append(' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title"><a href="/' + str(x.user_profile.slug) +'"> '
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

                    mail = str(user.email).lower()
                    if (mail.find('student')):
                        heading = 'Supervisors'
                    else:
                        heading = 'Students'
                    outputHTML.append('<div class="jumbotron"> <h2> '+ heading + ' </h2> \n')
                    for x in returned_users:
                        profile = UserProfile.objects.filter(user=x)[0]
                        isStaff = True

                        try:
                            userType = Supervisor.objects.filter(user_profile=profile)[0]
                            userTypeString = userType.job_title
                            print userType.job_title
                        except:
                            userType = Student.objects.filter(user_profile=profile)[0]
                            isStaff = False
                            userTypeString = 'Student'

                            print str(mail.find('student')) + ', ' + str(isStaff)
                        if (mail.find('student') == -1) and  (isStaff == False):
                            print "AUSIDBNAOSDI"
                        if ((mail.find('student') == -1) and  (isStaff == False)) or ((mail.find('student') != -1) and  (isStaff == True)):
                            print 'studentType'
                            print "SLUG: " + str(profile.slug)
                            outputHTML.append(
                                ' <div class="panel panel-success"> <div class="panel-heading"> <h3 class="panel-title"><a href="/' + str(profile.slug) +'"> '
                                + str(x.first_name) + ' ' + str(x.last_name) + ' (' + userTypeString + ')' + '</h3> </div><div '
                                'class="panel-body"> ' )
                                # HEADER

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
    else:
                return HttpResponseRedirect(reverse('login'))

'''#do we need separate view for edited version
def project(request):

def search(request):'''

def favorite_supervisor(request):

    if request.user.is_authenticated():
        user = request.user
        profile = UserProfile.objects.filter(user=user)[0]
        student = Student.objects.filter(user_profile = profile)[0]
        list = student.supervisor_choices.all()
        return render(request, 'FMS/search_results.html', {'found_users':list})

    else:
                return HttpResponseRedirect(reverse('login'))
