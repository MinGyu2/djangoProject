from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

# Create your views here.
from .models import Error   # db 접근
from .forms import UserForm

menu_list = ['설비 조회', '관리자 위치', '에러 로그', '직원 DB']

no_login_lastname = ['factory_machinery']
equipment_last_name = 'factory_machinery'
#---------------- main page --------------------------
def mainpage(request):
    if request.user.is_authenticated:
        # 이것 공장 장치로 로그인 되는것을 방지
        if request.user.last_name in no_login_lastname:
            return redirect('logout')
        context = {
            'menu_list': zip(menu_list, [1, 2, 3, 4]),
            'select_menu': menu_list[0],
        }
        # return HttpResponse("Hellow world!!123")
        return render(request, 'mainsite.html', context=context)
    else:
        return redirect('login')    # common 의 urls login 부분 의 이름
#-----------------------------------------------------

#---------------menu----------------------------------
def mainpage_menuselect(request,num):
    if request.user.is_authenticated:
        if num > 4 or num < 1:
            return HttpResponseRedirect('/apps/')
        context = {}
        if num == 1:    # menu_1.html
            # w = 0
            # num_value = request.session.get('weight_value', 0)
            # vvv = cache.get('tetet', 0)
            # request.session['weight_value'] = num_value+1

            equipment = User.objects.filter(last_name=equipment_last_name)
            equipment_names = [u.username for u in equipment]
            # equipment_names = ['프레스',1,2,3,4,4,5,6,7,8,9]
            orders = [k%4+1 for k in range(len(equipment_names))]
            con = get_redis_connection('default')
            item_of_list = []
            for eq in equipment_names:
                zips = zip([k.decode('utf-8') for k in con.hkeys(eq)],
                           [k.decode('utf-8') for k in con.hvals(eq)])
                item_of_list.append([(key, val) for key, val in zips])
            context = {
                'list': zip(equipment_names,
                            orders,
                            item_of_list),
            }
        elif num == 2:  #menu2
            # del request.session['weight_value']
            con = get_redis_connection("default")
            u = User.objects.filter(last_name=equipment_last_name)
            context = {
                # 'test': request.session['weight_value'],
                'test2': cache.get('tetet', 0),
                'test3': zip([k.decode('utf-8') for k in con.hkeys('asdf12')],
                             [k.decode('utf-8') for k in con.hvals('asdf12')]),
                'test4': u,
                'test5': [k.username for k in u],
            }
        elif num == 3:  # menu_3
            errors_num = Error.objects.all().count()
            items = Error.objects.order_by()
            context = {
                'errors_num': errors_num,
                'items': reversed(items),
            }
        return render(request, 'menu/menu_'+str(num)+'.html', context=context)
    else:
        return redirect('login')
#-----------------------------------------------------

#----------------- menu4 user delete,sign,search ---------------------------
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
                    if user.last_name in no_login_lastname:
                        context['one_msg'] = "아이디 존재 안함"
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
            'no_login_lastname': no_login_lastname,
        }
        return render(request, 'menu/menu_4.html', context=context)
    else:
        return HttpResponse("error")
# ----------------------------------------------------------------------------------


# -----------------------menu_1 post로 data 받기-----------------------------------


# 캐시에 저장 제외
not_store_in_cache = ['csrfmiddlewaretoken', 'user_id', 'user_pwd', 'equipment_name']


def menu1_receive_data(request):
    if request.method == "POST":
        form = request.POST
        # user 인지 검사
        s = form['user_id']
        p = form['user_pwd']
        user = authenticate(username=s, password=p)
        #
        # 장비 존재하는 검사하기 위한것
        equipment_name = form['equipment_name']
        eq_names = [u.username for u in User.objects.filter(last_name=equipment_last_name)]
        if user is not None and equipment_name in eq_names: # user인지 검사 and 존재하는 장비인지 확인
            con = get_redis_connection("default")
            h = {key: value for key, value in form.items() if key not in not_store_in_cache}
            con.delete(equipment_name)
            con.hmset(equipment_name, h)
            return HttpResponse(str(user) + " success! ")
        else:
            return HttpResponse("not_user or no_equipment_name")
    else:
        return HttpResponse("잘못된 접근")
# -----------------------menu_1 post로 data 받기-----------------------------------

#----------------------error 전송 받기-----------------------------------------
def receive_error_data(request):
    if request.method == "POST":
        form = request.POST
        # user 인지 검사
        s = form['user_id']
        p = form['user_pwd']
        user = authenticate(username=s, password=p)
        #
        # 존재하는 설비 인지 검사하기 위한것
        equipment_name = form['equipment_name']
        eq_names = [u.username for u in User.objects.filter(last_name=equipment_last_name)]
        if user is not None and equipment_name in eq_names:  # user인지 검사 and 존재하는 장비인지 확인
            error_content = form['error_content']
            e = Error(error_register_name= s,
                      error_equip_name= equipment_name,
                      error_content = error_content).save()
            return HttpResponse("성공")
        else:
            return HttpResponse("not_user or no_equipment_name")
    else:
        return Http404("잘못된 접근")
#-----------------------------------------------------------------------------

#----------------------모바일 로그인 확인------------------------------------------------
def only_login_value(request):
    if request.method == "POST":
        form = request.POST
        # user 인지 검사
        s = form['user_id']
        p = form['user_pwd']
        user = authenticate(username=s, password=p)
        if user is not None:  # user 인지 검사
            login(request, user)
            return HttpResponse("성공")
        else:
            return HttpResponse("유저아님")
    else:
        return Http404("잘못된 접근")
#------------------------------------------------------------------------------------