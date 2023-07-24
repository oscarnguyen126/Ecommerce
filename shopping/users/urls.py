from django.urls import path
from users import views
from shopping_app import views as shopping_views


urlpatterns = [
    path('<int:pk>/cart/', views.get_user_cart),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('register/', views.UserList.as_view()),
    path("<int:pk>/", views.UserDetails.as_view()),
]
