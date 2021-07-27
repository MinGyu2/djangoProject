from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from .models import Error   # db 접근
from .forms import UserForm, UserDelForm

menu_list = ['설비 조회', '관리자 위치', '에러 로그', '직원 DB']
def mainpage(request):
    if request.user.is_authenticated:
        num_errors = Error.objects.all().count()
        context = {
            # 'num_errors': num_errors,
            'menu_list': zip(menu_list, [1, 2, 3, 4]),
            'select_menu': menu_list[0],
        }
        # return HttpResponse("Hellow world!!123")
        return render(request, 'mainsite.html', context=context)
    else:
        return redirect('login')    # common 의 urls login 부분 의 이름

def mainpage_menuselect(request,num):
    if request.user.is_authenticated:
        if num > 4 or num < 1:
            return HttpResponseRedirect('/apps/')
        context = {}
        if num == 1:    # menu_1.html
            w = 0
            item_of_list = [[('무게1', w), ('test1', 3)],
                            [('무게2', w), ('test2', 4)],
                            [('무게3', w), ('test3', 5)],
                            [('무게4', w), ('test4', 6)]]
            context = {
                'list': zip(["프레스", "차체조립", "C", "D"],
                            [1, 2, 3, 4],
                            item_of_list),
            }
        return render(request, 'menu/menu_'+str(num)+'.html', context=context)
    else:
        return redirect('login')

def user_sign(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = UserForm()
        return render(request, 'menu/menu_4.html', {'form': form})
    else:
        return HttpResponse("error")

def user_del(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = request.POST
            context = {}
            if form['user_id'] == '':
                context['msg'] = '삭제할 아이디를 입력하세요'
            else:
                try:
                    user = User.objects.get(username=form['user_id'])
                    user.delete()
                    context['msg'] = "삭제 성공"
                except User.DoesNotExist:
                    context['msg'] = "아이디 존재 안함"
                except Exception as e:
                    context['msg'] = e
            return render(request, 'menu/menu_4.html', context=context)
        else:
            return HttpResponse("Not POST")
    else:
        return HttpResponse("error")

def one_search_user_id(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = request.POST
            context = {}
            if form['user_id'] == '':
                context['one_msg'] = '검색할 아이디를 입력하세요'
            else:
                try:
                    user = User.objects.get(username=form['user_id'])
                    context['one_user'] = user
                except User.DoesNotExist:
                    context['one_msg'] = "아이디 존재 안함"
                except Exception as e:
                    context['one_msg'] = e
                context['one_user_info_order'] = ['아이디', '이름', '이메일']
            return render(request, 'menu/menu_4.html', context=context)
        else:
            return HttpResponse("Not POST")
    else:
        return HttpResponse("error")

def all_search_user_id(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        context = {
            'user_all_id': users,
            'user_info_order': ['아이디', '이름', '이메일'],
                 }
        return render(request, 'menu/menu_4.html', context=context)
    else:
        return HttpResponse("error")