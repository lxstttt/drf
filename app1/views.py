from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import Book
from app1.serializers import BookModelSerializer, BookModelDeSerializer, BookModelSerializerV2


class BookAPIView(APIView):
    '''
    查询图书信息
    '''
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get('id')
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            print(book_obj)
            book_md_ser = BookModelSerializer(book_obj).data
            return Response({
                'status': 200,
                'msg': '查询单个',
                'rst': book_md_ser,
            })
        else:
            book_all = Book.objects.all()
            book_md_ser = BookModelSerializer(book_all,many=True).data
            return Response({
                'status': 201,
                'msg': '查询所有成功',
                'rst': book_md_ser
            })

    def post(self,request,*args,**kwargs):

        data = request.data
        # print(data)

        data_ser = BookModelDeSerializer(data=data)
        # 校验数据是否合法 raise_exception=True  一旦校验失败 立即抛出异常
        data_ser.is_valid(raise_exception=True)
        book_obj = data_ser.save()

        return Response({
            "status": 202,
            "msg": "创建图书成功",
            "results": BookModelSerializer(book_obj).data
        })

class BookAPIView2(APIView):

    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
            book_ser = BookModelSerializerV2(book_obj).data
            return Response({
                "status": 200,
                "msg": "查询单个图书成功",
                "results": book_ser
            })
        else:
            book_all = Book.objects.filter(is_delete=False)
            book_ser = BookModelSerializerV2(book_all, many=True).data
            return Response({
                "status": 200,
                "msg": "查询所有成功",
                'results': book_ser
            })

    def post(self, request, *args, **kwargs):
        """
        新增单个：传递参数的格式 字典
        新增多个：[{},{},{}]  列表中嵌套字典  每一个字典是一个图书对象
        :param request:
        :return:
        """
        request_data = request.data
        if isinstance(request_data, dict):  # 代表添加单个对象
            many = False
        elif isinstance(request_data, list):  # 代表添加多个对象
            many = True
        else:
            return Response({
                "status": 400,
                "message": "数据格式有误"
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": '添加图书成功',
            "results": BookModelSerializerV2(save, many=many).data
        })

    def delete(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id: # 单个
            ids = [book_id]
        else: # 多个
            ids = request.data.get("ids")
            print(ids)

        # 判断传递过来的图书的id是否在数据库中  且还未删除
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或者图书不存在",
        })

    def put(self, request, *args, **kwargs):
        """
        整体修改单个：修改一个对象的全部字段
        :return 修改后的对象
        """
        # 修改的参数
        request_data = request.data
        # 要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在",
            })

        # instance-指定修改对象    数据修改前校验
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": BookModelSerializerV2(save).data
        })


    def patch(self, request, *args, **kwargs):
        """
        局部更新
        """

        request_data = request.data

        book_id = kwargs.get("id")

        # try:
        #     book_obj = Book.objects.get(pk=book_id)
        # except:
        #     return Response({
        #         "status": status.HTTP_400_BAD_REQUEST,
        #         "message": "图书不存在",
        #     })
        #
        # # 前端发送的修改的值需要做安全校验
        # # 更新参数的时候使用序列化器完成数据的校验
        # # TODO 如果当前要局部修改则需指定 partial = True即可
        # book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        # book_ser.is_valid(raise_exception=True)
        # save = book_ser.save()
        #
        # return Response({
        #     "status": 200,
        #     "message": "更新成功",
        #     "results": BookModelSerializerV2(save).data
        # })
        if book_id and isinstance(request_data,dict):
            # 代表修改单个
            book_ids = [book_id,]
            book_data = [request_data,]
        elif not book_id and isinstance(request_data,list):
            book_ids = []

            for dic in request_data:
                id = dic.pop('id',None)
                if id:
                    book_ids.append(id)
                else:
                    return Response({
                        "status":status.HTTP_400_BAD_REQUEST,
                        "msg":'id不存在'
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })

        book_list = []

        for pk in book_ids:
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
            except:
                index = book_ids.index(pk)
                request_data.pop(index)

        book_ser = BookModelSerializerV2(data=request_data, instance=book_list,
                                         partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",
            "results": BookModelSerializerV2(save)
        })

