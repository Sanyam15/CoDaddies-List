from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,template_name='base.html')

def new_search(request):
    search=request.POST.get('searchy')
    print(search)
    stuff_for_frontend={'search':search
                        }
    return render(request,template_name='my_app/new_search.html',context=stuff_for_frontend)