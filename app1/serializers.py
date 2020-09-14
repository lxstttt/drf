from rest_framework import serializers
from rest_framework.serializers import Serializer

from app1.models import User
from drf_day3 import settings
from rest_framework import exceptions


class UserSerializer(Serializer): # 序列化器与每一个model对应

    username = serializers.CharField()
    pwd = serializers.CharField()
    # gender = serializers.IntegerField()
    email = serializers.CharField()
    # pic = serializers.ImageField()

    # 定义models中不存在的字段  SerializerMethodField()
    # 自定义字段  返回一个盐
    salt = serializers.SerializerMethodField()

    # 自定义性别字段的返回值
    gender = serializers.SerializerMethodField()

    # self: 当前序列化器 obj：当前对象
    def get_gender(self, obj):

        return obj.get_gender_display()

    # 自定义图片返回的全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):

        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, obj.pic)

class UserDeSerializer(serializers.Serializer):
    """
    反序列化：将前端提交的数据保存入库
    1. 前端需要提供哪些字段
    2. 对前端提供数据做安全校验
    3. 哪些字段需要一些额外的安全校验
    反序列化是不存在自定义字段的
    """
    # 可以在字段中添加校验规则

    username = serializers.CharField(
        max_length=10,
        min_length=2,
        # 为规则自定义错误信息
        error_messages={
            "max_length": "用户名过长",
            "min_length": "用户名过短"
        }
    )
    pwd = serializers.CharField()
    email = serializers.CharField(min_length=8, required=True)


    # 自定义字段  重复密码
    re_pwd = serializers.CharField()

    # 安全校验
    # TODO 在create保存对象之前  DRF提供了两个钩子函数来对数据进行校验

    # 局部钩子： 可以对反序列化中的某个字段进行校验
    # validate_想验证的字段名
    def validate_username(self, value):
        # print("1111", value, type(value))
        if "小" in value:
            raise exceptions.ValidationError("用户名有误")

        return value

    # 全局钩子  可以通过attrs获取到所有的参数
    def validate(self, attrs):
        # print("22222", attrs)
        pwd = attrs.get("pwd")
        re_pwd = attrs.pop("re_pwd")
        # print(attrs)
        # 自定义校验规则  两次密码不一致  则无法保存对象
        if pwd != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")

        return attrs

    def create(self, validated_data):
        """
        在保存用户对象时需要重写此方法完成保存
        :param validated_data: 前端传递的需要保存的数据
        :return:
        """
        # print(validated_data)
        return User.objects.create(**validated_data)