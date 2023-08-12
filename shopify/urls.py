from django.urls import path
from shopify import views

urlpatterns = [
    
     path('register/', views.register_user),
     path('login/', views.login_user),
     path('logout/', views.logout_user),
     path('addcategory/',views.add_category),
     path('additem/',views.add_item),
     path('getitem/',views.get_item),
  
]
