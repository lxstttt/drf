from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import User

#drf 模块
from rest_framework import views
from rest_framework import response
from rest_framework import request
from rest_framework import serializers


@csrf_exempt  # 为某个视图免除csrf保护
def hello(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        print(name)
        return HttpResponse('get请求收到')

    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)
        return HttpResponse('post请求收到')

    if request.method == 'PUT':
        # name = request.PUT.get('name')
        # print(name)
        return HttpResponse('put请求收到')

    if request.method == 'DELETE':
        # name = request.DELETE.get('name')
        # print(name)
        return HttpResponse('delete请求收到')


@method_decorator(csrf_exempt,name='dispatch')
class UserView(View):
    '''
    django类视图
    '''
    def get(self,request,*args,**kwargs):
        print('get的请求查询')
        return HttpResponse('get访问成功')

    def post(self,request,*args,**kwargs):
        print('post的请求查询')
        return HttpResponse('post访问成功')

    def put(self,request,*args,**kwargs):
        print('put的请求查询')
        return HttpResponse('put访问成功')

    def delete(self,request,*args,**kwargs):
        print('delete的请求查询')
        return HttpResponse('delete访问成功')


@method_decorator(csrf_exempt,name='dispatch')
class Djl(View):
    def get(self,request,*args,**kwargs):
        '''
        查询用户接口
        :param request:请求对象
        :param args:
        :param kwargs:
        :return: 结果
        '''
        user_id = kwargs.get('id')
        if user_id:
            # obj = User.objects.filter(pk=user_id)
            obj = User.objects.filter(pk=user_id).values('username','pwd','email').first()
            print(obj)
            if obj:## 若查询到，讲信息返回到前端
                return JsonResponse({
                    'status':'200',
                    'msg':'查询单个用户成功',
                    'rst':obj,
                })
        else:#id为空代表查所有用户
            user_list = User.objects.all().values('username','pwd','email')
            print(user_list)
            return JsonResponse({
                'status':200,
                'msg':'查询所有用户',
                'rst':list(user_list),
            })
        return JsonResponse({
            'status':500,
            'msg':'查询失败'
        })

    def post(self, request, *args, **kwargs):
        """
        新增单个用户的接口
        :param request: 用户输入的信息
        :return:
        """
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        email = request.POST.get("email")

        try:
            user_obj = User.objects.create(username=username, pwd=pwd, email=email)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "email": user_obj.email}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })



class UserAPI(APIView):

    def get(self,request,*args,**kwargs):
        user_id = kwargs.get('id')
        if user_id:
            # obj = User.objects.filter(pk=user_id)
            obj = User.objects.filter(pk=user_id).values('username','pwd','email').first()
            print(obj)
            if obj:## 若查询到，讲信息返回到前端
                return JsonResponse({
                    'status':'200',
                    'msg':'查询单个用户成功',
                    'rst':obj,
                })
        else:  # id为空代表查所有用户
            user_list = User.objects.all().values('username', 'pwd', 'email')
            print(user_list)
            return JsonResponse({
                'status': 200,
                'msg': '查询所有用户',
                'rst': list(user_list),
                })
        return JsonResponse({
            'status': 500,
            'msg': '查询失败'
        })


    def post(self, request, *args, **kwargs):
        """
        新增单个用户的接口
        :param request: 用户输入的信息
        :return:
        """
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        email = request.POST.get("email")
        print(username)
        # return Response('1')

        try:
            user_obj = User.objects.create(username=username, pwd=pwd, email=email)
            return JsonResponse({
                "status": 200,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "email": user_obj.email}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })


