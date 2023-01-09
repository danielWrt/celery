from django.urls import path, include

from .views import RegisterUserView, activate_view


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', activate_view),
]