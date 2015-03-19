from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "Hello World!"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'FMS/index.html', context_dict)

#do we need separate view for edited version
def profile(request):

#do we need separate view for edited version
def project(request):

def search(request):