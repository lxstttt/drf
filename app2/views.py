from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from app2.models import Student
from utils.response import APIResponse
from .serializers import StudentModelSerializer

# Create your views here.

class StudentAPIView(APIView):

    def get(self,request,*args,**kwargs):

        obj_all = Student.objects.all()
        ser = StudentModelSerializer(obj_all,many=True).data
        return APIResponse(results=ser)


class StudentGenericAPIView(
                         ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    # 获取当前视图操作的模型的数据  以及序列化器类
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer


    # 指定查询单个对象的参数
    lookup_field = "id"

    #查询接口
    def get(self,request,*args,**kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    # 新增学生
    def post(self, request, *args, **kwargs):
        create = self.create(request, *args, **kwargs)
        return APIResponse(results=create.data, data_message="新增学生快捷方式")

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class StudentGenericMixinView(ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer
    lookup_field = "id"

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer
    lookup_field = "id"
    def user_login(self, request, *args, **kwargs):
        # 用户登录
        request_data = request.data
        print(request_data,request_data.get('stu_name'))
        name = request_data.get("stu_name")
        pwd = request_data.get('pwd')
        if name and pwd:
            return APIResponse(data_message="登录成功")
        else:
            return APIResponse(data_message="登录失败")

    def user_register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)