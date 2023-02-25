from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated
import jwt
import flutterdjango.settings
from rest_framework import exceptions
from .models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from datetime import timedelta,datetime
from .extraAuth import ValidateKey
# Generate Token Manually

def decode_refresh_token(token):
  try:
    payload = jwt.decode(token,'django-insecure-36oq%)!rnny59^t_4er6ivpg!@15!jm+imp$$7gjr$vhv&q#&9',algorithms='HS256')
    return payload['user_id']
  except:
    raise exceptions.AuthenticationFailed('unauthenticated')
  

def expires_in(token):
    payload = jwt.decode(token,'django-insecure-36oq%)!rnny59^t_4er6ivpg!@15!jm+imp$$7gjr$vhv&q#&9',algorithms='HS256')
    
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  payload = jwt.decode(str(refresh.access_token),'django-insecure-36oq%)!rnny59^t_4er6ivpg!@15!jm+imp$$7gjr$vhv&q#&9',algorithms='HS256')
  refreshTime = jwt.decode(str(refresh),'django-insecure-36oq%)!rnny59^t_4er6ivpg!@15!jm+imp$$7gjr$vhv&q#&9',algorithms='HS256')
  # print(f"Expires Time is    {datetime.ut}")
  iat_datetime = refresh.access_token['iat']
  exp_datetime = refresh.access_token['exp']
  token_duration = int((exp_datetime - iat_datetime))
  

  refresh_iat_datetime = refresh['iat']
  refresh_exp_datetime = refresh['exp']
  refresh_token_duration = int((refresh_exp_datetime - refresh_iat_datetime))


  print(f'Access token time is {token_duration}')
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      # 'token_duration' : int((refresh.access_token['exp'] - refresh.access_token['iat']).total_seconds()),
      'accessTokenExpriry':int(token_duration),
      'refreshTokenExpriry':int(refresh_token_duration),
  }



class UserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'status':status.HTTP_201_CREATED, 'message':'Registration Successful','accessToken':token}, )
    return Response({ 'msg':'Registration Faild'}, status=status.HTTP_400_BAD_REQUEST)


class RefreshAccessTokenView(APIView):
  def post(self, request, format=None):
    refres_token = request.data.get('refreshToken')
    id =decode_refresh_token(refres_token)
    # print(f"User id is {type()}")
    user = User.objects.get(id = id)
    token = get_tokens_for_user(user)
    return Response({'status':status.HTTP_200_OK, 'message':'Access token refreshed','data':token}, )





class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        print(f"User is    {user}")
        token = get_tokens_for_user(user)
        access_token = AccessToken(token.get('access'))
        user1 = User.objects.get(id = access_token.get('user_id'))
        userSerializer = UserProfileSerializer(user1)
        return Response({'status':status.HTTP_200_OK, 'message':'Login Successful','data':token,'userDetails':userSerializer.data}, )
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    print(f"I am here    {serializer.data}")
    return Response({'status':status.HTTP_200_OK,'message':"Given the profile successfully",'data':serializer.data})

    


class UserProfileEditView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk = None, format = None):
      stu = User.objects.get(id = request.auth['user_id'])
      serializer = UserProfileSerializer(stu, data = request.data, partial = True)
      if serializer.is_valid():
          serializer.save()
          return Response({'status':status.HTTP_200_OK,'message':'User edited!'})
      return Response(serializer.errors)
    