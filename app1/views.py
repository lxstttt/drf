from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,UpdateModelMixin
# Create your views here.
from rest_framework.views import APIView

from app1.models import User, Employee
from app1.serializers import UserModelSerializer, EmployeeModelSerializer, UserModelSerializer2
from utils.response import APIResponse


class UserAPIView(APIView):

    # 处理用户注册
    def post(self,request,*args,**kwargs):

        data = request.data
        serializer = UserModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        save = serializer.save()
        return APIResponse(200, True, results=UserModelSerializer(save).data)

    # # 处理用户登录
    # def get(self,request,*args,**kwargs):
    #
    #     username = request.query_params.get('username')
    #     pwd = request.query_params.get('pwd')
    #     print(username,pwd)
    #
    #     user_obj = User.objects.filter(username=username, password=pwd).first()
    #     if user_obj:
    #         data = UserModelSerializer(user_obj).data
    #         return APIResponse(200, True, results=data)

        # return APIResponse(400, False)

class EmployeeGenericAPIView(ListModelMixin, CreateModelMixin, GenericAPIView,DestroyModelMixin,UpdateModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeModelSerializer

    lookup_field = 'id'

    # 处理获取员工请求
    def get(self,request,*args,**kwargs):
        response = self.list(request,*args,**kwargs)
        return APIResponse(200, True, results=response.data)

    # 处理员工添加请求
    def post(self,request,*args,**kwargs):
        print(request.data)
        response = self.create(request,*args,**kwargs)
        return APIResponse(200, True, results=response.data)

    # 处理删除员工请求
    def delete(self,request,*args,**kwargs):
        # id = request.data.get('id')
        # print(id)
        # lookup_field = id
        response = self.destroy(request, *args, **kwargs)
        return APIResponse(200, True, results=response.data)


    # #处理更新员工请求
    # def patch(self,request,*args,**kwargs):
    #     response = self.partial_update(request, *args, **kwargs)
    #     return APIResponse(200, True, results=response.data)

class LoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    # 处理用户登录并签发token
    def post(self, request, *args, **kwargs):

        # 账号使用account 接收  密码使用pwd接收
        # account = request.data.get("account")
        # pwd = request.data.get("pwd")
        # print(account, pwd)

        serializer = UserModelSerializer2(data=request.data)

        serializer.is_valid(raise_exception=True)
        #
        # obj_data = UserModelSerializer2(serializer.obj).data
        return APIResponse(data_message='OK',token = serializer.token,results=UserModelSerializer2(serializer.obj).data)

class EmpUpdateAPIView(GenericAPIView,UpdateModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeModelSerializer

    lookup_field = 'id'

    #处理更新员工请求
    def patch(self,request,*args,**kwargs):
        print('来更新了')
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(200, True, results=response.data)