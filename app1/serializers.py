from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import exceptions
from app1.models import Book, Press


# 出版社的序列号器
class PressModelSerializer(ModelSerializer):

    class Meta:
        model = Press
        fields = ("press_name", 'address')

# 图书的序列化器
class BookModelSerializer(ModelSerializer):

    publish = PressModelSerializer()

    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "publish",'author_list')

        # 可以直接查询表的所有字段
        # fields = "__all__"

        # 指定不展示哪些字段
        # exclude = ("is_delete", "status", "id")

        # # 指定查询的深度
        # depth = 1


#图书反序列化器
class BookModelDeSerializer(ModelSerializer):

    publish = PressModelSerializer()

    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")
        # 为反序列化添加校验准则
        extra_kwargs = {
            "book_name": {
                "max_length": 18,
                "min_length": 1,
                "error_messages": {
                    "max_length": "图书名过长",
                    "min_length": "图书名过短",
                }
            },
            "price": {
                "required": True,
                "decimal_places": 2,
            }
        }

    # 全局钩子同样适用于 ModelSerializer
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs

    # 局部钩子的使用
    def validate_price(self, obj):
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过1000")
        return obj

class BookListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成多个对象同时修改
    """
    # 重写update方法完成更新
    def update(self, instance, validated_data):
        # instance 要修改的对象
        # validated_data 要修改的值
        print(self,instance,validated_data,self.child)

        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
            return instance

# 序列化器与反序列化器整合
class BookModelSerializerV2(ModelSerializer):


    class Meta:

        list_serializer_class = BookListSerializer
        model = Book
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("book_name", "price", "pic", "publish", "authors",'press_name','author_list')

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            "book_name": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
            },
            # 只参与反序列化
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            },
            "press_name": {
                "read_only": True
            },
            "author_list":{
                "read_only":True
            }
        }

    # 全局钩子同样适用于 ModelSerializer
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs


    # 局部钩子的使用  验证每个字段
    def validate_price(self, obj):
        # 价格不能超过1000
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过10000")
        return obj

    # # 重写update方法完成更新  --可根据自己选择，系统底层自更新
    # def update(self, instance, validated_data):
    #     print(instance, "11111")
    #     print(validated_data)
    #     book_name = validated_data.get("book_name")
    #     instance.book_name = book_name
    #     instance.save()
    #     return instance




