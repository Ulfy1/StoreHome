from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'title': 'Home - main',
        'content':  'HOME Furniture Store',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - about',
        'content':  'About us',
        'text_on_page': "Reason why this shop is nice"
    }
    return render(request, 'main/about.html', context)