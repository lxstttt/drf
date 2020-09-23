from rest_framework.serializers import ModelSerializer

from app2.models import Tree



class TreeModelSerializer(ModelSerializer):

    class Meta:

        model = Tree
        fields = '__all__'