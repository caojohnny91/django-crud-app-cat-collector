from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("cats/", views.cat_index, name="cat-index"),
    path("cats/<int:cat_id>/", views.cat_detail, name="cat-detail"),
    # Mounts main_app's routes at the root URL
    # new route used to create a cat
    path("cats/create/", views.CatCreate.as_view(), name="cat-create"),
    path("cats/<int:pk>/update/", views.CatUpdate.as_view(), name="cat-update"),
    path("cats/<int:pk>/delete/", views.CatDelete.as_view(), name="cat-delete"),
    path("cats/<int:cat_id>/add-feeding/", views.add_feeding, name="add-feeding"),
    # The above route specifies that the <form>’s action attribute will need to look something like /cats/2/add-feeding. Let’s update the form now.
]
