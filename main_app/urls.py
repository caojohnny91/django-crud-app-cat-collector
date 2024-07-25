from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("cats/", views.cat_index, name="cat-index"),
    path("cats/<int:cat_id>/", views.cat_detail, name="cat-detail"),
  # Mounts main_app's routes at the root URL
    # new route used to create a cat
    path('cats/create/', views.CatCreate.as_view(), name='cat-create'),
]    
