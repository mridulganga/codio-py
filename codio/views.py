from django.shortcuts import render
from django.utils import timezone
from .models import code
from django.db.models import Q
from .forms import submit_form
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import string
# Create your views here.

def code_list(request):
    code_list = code.objects.all().order_by('-add_date')
    content = {
    'code_list':code_list,
    'page_title':'Codes',
    }
    return render(request, 'code-list.html', content)

def code_single(request,code_id):
    code_single = code.objects.get(id=int(code_id))
    tags = code_single.tags.split(",")
    return render(request, 'code-single.html',{'code':code_single, 'tags':tags, })


def home(request):
    return render(request,'index.html')




def search_tag(request,tag):
    code_list = code.objects.filter(tags__contains=tag).order_by('add_date')
    content = {
    'code_list':code_list,
    'page_title':'Search - Tag',
    }
    return render(request, 'code-list.html', content)

def search_lang(request,lang):
    code_list = code.objects.filter(language=lang).order_by('add_date')
    content = {
    'code_list':code_list,
    'page_title':'Search - Language',
    }
    return render(request, 'code-list.html', content)

def search_dev(request,dev):
    code_list = code.objects.filter(developer=dev).order_by('add_date')
    content = {
    'code_list':code_list,
    'page_title':'Search - Developer',
    }
    return render(request, 'code-list.html', content)

def search(request):
    if request.method == 'POST':
        results = code.objects.all()
        searches = request.POST.get('q', "")
        for search in searches.split(" "):
            if search:
                results = results.filter(title__contains=search) | results.filter(language__contains=search) | \
                results.filter(tags__contains=search) | results.filter(usage__contains=search) | results.filter(code_text__contains=search)
            content = {
            'code_list':results,
            'page_title':'Search',
            }
        return render(request, 'code-list.html', content)
    else:
        return HttpResponseRedirect('/view/list')


def user_profile(request,user_id=0):
    if user_id==0:
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return HttpResponseRedirect('/view/list/')

    code_list = code.objects.filter(developer=user_id)
    no_codes = code_list.count()
    return render(request,'user-profile.html',{'no_codes':no_codes,})

def user_codes(request,user_id=0):
    if user_id==0:
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return HttpResponseRedirect('/view/list/')
    code_list = code.objects.filter(developer=user_id)
    content = {
        'code_list':code_list,
        'page_title': str(User.objects.get(pk=user_id)) + ' - Submissions',
        }
    return render(request,'code-list.html',content)





def edit_code(request,code_id):
    ecode = code.objects.get(id=code_id)
    if request.method == 'POST':
        ecode.title = request.POST.get("title",ecode.title)
        ecode.usage = request.POST.get("usage", ecode.usage)
        ecode.code_text = request.POST.get("code_text", ecode.code_text)
        ecode.input_output = request.POST.get("input_output", ecode.input_output)
        ecode.tags = request.POST.get("tags", ecode.tags)
        ecode.level = request.POST.get("level",ecode.level)
        ecode.save()
    return HttpResponseRedirect('/view/single/' + str(code_id))

def remove_code(request,code_id):
    ecode = code.objects.get(id=code_id).delete()
    return HttpResponseRedirect('/view/list/')

def submit_code(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = submit_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            code = form.save(commit=False)
            code.language = request.POST.get("language")
            code.developer = request.user
            code.add_date = timezone.now()
            code.level = request.POST.get("level")
            code.save()
            code_id = code.id
            return HttpResponseRedirect('/view/single/' + str(code_id))
    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_authenticated():
            form = submit_form()
            return render(request, 'submit-code.html', {'form': form})
        else:
            return HttpResponseRedirect('/admin/login/?next=/submit-code/')
