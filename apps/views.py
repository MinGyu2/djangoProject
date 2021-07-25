from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from .models import Error   # db 접근

menu_list = ['설비 조회', '관리자 위치', '에러 로그', '직원 DB']
def mainpage(request):
    num_errors = Error.objects.all().count()
    context = {
        # 'num_errors': num_errors,
        'menu_list': zip(menu_list, [1, 2, 3, 4]),
        'select_menu': menu_list[0],
    }
    # return HttpResponse("Hellow world!!123")
    return render(request, 'mainsite.html', context=context)

def mainpage_menuselect(request,num):
    if num > 4 or num < 1:
        return HttpResponseRedirect('/apps/')
    context = {
        'menu_list': zip(menu_list, [1, 2, 3, 4]),
        'select_menu': menu_list[num-1],
    }
    return render(request, 'menu/menu_'+str(num)+'.html', context=context)
