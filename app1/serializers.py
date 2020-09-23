from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions, serializers

import re

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from app1.models import User, Employee


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','real_name','gender')

        extra_kwargs = {
            "username": {
                'required': True,
                'min_length': 2,
                "error_messages": {
                    'required': '用户名必填',
                    'min_length': '用户长度不够'
                },
                # "read_only":True,
            },
            "password":{
                "write_only":True,
            }
        }

    def validate_username(self, attrs):
        user = User.objects.filter(username=attrs).first()

        if user:
            raise exceptions.ValidationError("用户名已存在")

        return attrs


class EmployeeModelSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

        extra_kwargs = {
            "emp_name": {
                'required': True,
                'min_length': 2,
                "error_messages": {
                    'required': '用户名必填',
                    'min_length': '用户长度不够'
                }
            }
        }

class UserModelSerializer2(ModelSerializer):

    account = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ "account","pwd", "username","email"]

        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            },
        }

    # 完成token的生成
    def validate(self, attrs):
        account = attrs.get("account")
        pwd = attrs.get("pwd")

        # 对于前端传递的参数格式进行验证  邮箱  用户名
        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()
#
        # 判断用户是否存在 且用户密码是否正确
        if user_obj and user_obj.check_password(pwd):
            # 签发token
            payload = jwt_payload_handler(user_obj)  # 生成载荷
            token = jwt_encode_handler(payload)  # 生成token
            print(payload)
            self.token = token

            self.obj = user_obj

        return attrs