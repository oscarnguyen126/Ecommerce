from django.urls import path
from shopping_app import views


urlpatterns = [
    path('item/', views.ItemList.as_view()),
    path("item/<int:pk>/", views.ItemDetails.as_view()),
    path("category/", views.CategoryList.as_view()),
    path("category/<int:pk>/", views.CategoryDetails.as_view()),
]