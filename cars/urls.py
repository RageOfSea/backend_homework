from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/create/', views.car_create, name='car_create'),
    path('car/edit/<int:car_id>/', views.car_edit, name='car_edit'),
    path('car/delete/<int:car_id>/', views.car_delete, name='car_delete'),
    path('api/cars/', views.CarListView.as_view(), name='car_list_api'),
    path('api/cars/<int:id>/', views.CarDetailView.as_view(), name='car_detail_api'),
    path('api/cars/<int:car_id>/comments/', views.CommentListView.as_view(), name='comment_list_api'),
    path('api/cars/<int:car_id>/comments/<int:id>/', views.CommentDetailView.as_view(), name='comment_detail_api'),
    path('api/register/', views.register, name='register'),

]

