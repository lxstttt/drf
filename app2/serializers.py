from rest_framework.serializers import ModelSerializer

from app2.models import Student
from app1.serializers import BookListSerializer


class StudentModelSerializer(ModelSerializer):
    """
    序列化器与反序列化器整合
    """

    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = BookListSerializer

        model = Student
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("stu_name", "age", "pic", "gender", "in_class")

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            "stu_name": {
                "max_length": 4,  # 设置当前字段的最大长度
                "min_length": 2,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            }
        }