from django.urls import path
from .views import RegisterApiview, LoginApiView, UpdateUserApiView, GetEmployeeApiview, SkillListCreateApi, SkillGetbyidUpdateDeleteApi
from knox import views as knox_view


urlpatterns = [
    path('register/', RegisterApiview.as_view(), name="register"),
    path('login/', LoginApiView.as_view(), name="login"),
    path('update/', UpdateUserApiView.as_view(), name="update"),
    path('GetAll/', GetEmployeeApiview.as_view(), name="get"),
    path('skill/', SkillListCreateApi.as_view(), name='skill_list'),
    path('skill/<int:id>', SkillGetbyidUpdateDeleteApi.as_view(),
         name='skill_list_update')

]
