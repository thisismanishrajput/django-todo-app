from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TodoSerializer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User
from .models import TodoModel
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
import jwt


class TodoView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
        user = request.data.get('created_by')
        data = request.data
        data['created_by'] = User.objects.get(id = user)
        new_todo = TodoModel.objects.create(title = data['title'], desc = data['desc'], created_by = data['created_by'])
        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            new_todo.save()
            return Response({'status':status.HTTP_201_CREATED,'message':'Todo created successfully!'})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Todo creation failed'})

  def delete(self, request, pk = None, format = None):
    
    id = request.data.get('id')
    stu = TodoModel.objects.get(id = id)
    stu.delete()
    return Response({'status':status.HTTP_200_OK,'message':'Todo deleted success!'})
  
  def patch(self, request, pk = None, format = None):
    
    id = request.data.get('id')
    stu = TodoModel.objects.get(id = id)
    serializer = TodoSerializer(stu, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK,'message':'Todo updated!'})
    return Response(serializer.errors)




class TodoGetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk = None, format = None):
        # user1 = User.objects.get(id = request.data.get('id'))
        stu = TodoModel.objects.filter(created_by = request.auth['user_id'])
        serializer = TodoSerializer(stu,  many = True)
        return Response({'status':status.HTTP_200_OK,'message':'Given all todo successfully','data':serializer.data})


