from django.shortcuts import render

def index(request):
    return render(request, 'ia_app/index.html')
