from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from NFBasic.models import Notification, Announcement

a_list = Announcement.objects.all()
ac_1 = a_list[len(a_list) - 1]
ac_2 = a_list[len(a_list) - 2]
ac_3 = a_list[len(a_list) - 3]

def index(request):
    n_list = Notification.objects.order_by('-n_date')[:10]
    context = RequestContext(request, {
        'request': request,
        'nf_list': n_list,
        'ac_list': a_list,
        'ac_1': ac_1,
        'ac_2': ac_2,
        'ac_3': ac_3
    })
    return render(request, 'notifier/index.html', context)

def login_v(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if(user is not None):
        login(request, user)
        return render(request, 'notifier/loged.html')
    else:
        return render(request, 'notifier/re_log.html')

def logout_v(request):
    logout(request)
    return render(request, 'notifier/logout.html')

def detailIndex(request):
    a = request.GET['index']
    if(a == "first"):
        context = RequestContext(request, {
            'ac_dt': ac_1
        })
    if(a == "second"):
        context = RequestContext(request, {
            'ac_dt': ac_2
        })
    if(a == "third"):
        context = RequestContext(request, {
            'ac_dt': ac_3
        })
    return render(request, 'notifier/ac_detail.html', context)



