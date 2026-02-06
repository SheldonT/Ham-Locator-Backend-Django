
from django.urls import path
from keystone.views.CreateUser import CreateUserView
from keystone.views.Login import LoginView
from keystone.views.EditUser import EditUserView
from keystone.views.GetUser import GetUserView
from keystone.views.Logout import LogoutView
from keystone.views.RefreshTokens import RefreshTokensView

urlpatterns = [
    path('', LoginView.as_view()),
    path('adduser/', CreateUserView.as_view()),
    path('edituser/', EditUserView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh-tokens/', RefreshTokensView.as_view()),
]
