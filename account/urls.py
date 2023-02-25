from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserProfileView,RefreshAccessTokenView,UserProfileEditView
from todo.views import TodoView,TodoGetView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('get-profile/', UserProfileView.as_view(), name='get profile'),
    path('edit-profile/', UserProfileEditView.as_view(), name='edit profile'),
    path('add-todo/', TodoView.as_view(), name='add todo'),
    path('get-todo/', TodoGetView.as_view(), name='get todo'),
    path('delete-todo/', TodoView.as_view(), name='delete todo'),
    path('edit-todo/', TodoView.as_view(), name='edit todo'),
    path('refresh/', RefreshAccessTokenView.as_view(), name='refresh'),

]