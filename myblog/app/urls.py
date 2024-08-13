from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("",views.index, name="index"),
    path("posts", views.index, name="post"),
    path("new-post", views.create_post, name="create-post"),
    path("<int:id>", views.display_post, name="detail"),
    path("posts/<int:id>/edit", views.edit_post, name="update"),
    path("posts/<int:id>/delete", views.delete_post, name="delete"),
    path("login", views.login_author, name="login"),
    path("create-author", views.create_author, name="create"),
    path("logout", views.logout, name="logout")
]
