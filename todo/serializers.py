from rest_framework import serializers
from .models import TodoModel


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields = ["id", "title", "desc","created_at","updated_at",'created_by']
        depth = 1

    def __str__(self):
        return self.name
