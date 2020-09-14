from django.shortcuts import render
from rest_framework import status
from rest_framework.serializers import Serializer
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from app1.models import User
from app1.serializers import UserSerializer, UserDeSerializer


class UserAPIView(APIView):
    """
    查询接口
    :param request:
    :return:
    """

    def get(self,request,*args,**kwargs):

        user_id = kwargs.get('id')

        if user_id:
            # user_obj = User.objects.filter(pk=user_id).values('username','pwd','gender','email').first()
            user_obj = User.objects.filter(pk=user_id)
            user_ser = UserSerializer(user_obj).data

            return Response({
                'status':200,
                'msg':'查询单个',
                'rst':user_ser,
            })

        else:
            user_obj = User.objects.all()
            user_ser = UserSerializer(user_obj,many=True).data
            return Response({
                'status':201,
                'msg':'查询所有',
                'rst':user_ser,
            })

    def post(self,request,*args,**kwargs):

        user_data = request.data
        # 入库校验
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "msg": "请求数据有误"
            })

        ser = UserDeSerializer(data=user_data)

        if ser.is_valid():
            # 数据校验通过后才进行保存  调用save()保存数据  需要在序列化器中重写create()方法完成数据的入库
            user_obj = ser.save()

            return Response({
                "status": status.HTTP_200_OK,
                "msg": "用户添加成功",
                "rst": UserSerializer(user_obj).data
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "msg": ser.errors
        })