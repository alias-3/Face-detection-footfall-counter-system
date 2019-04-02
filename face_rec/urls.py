from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name='home'),
	# path("blog_list/",views.blog_list,name= 'blog_list'),
	# path("blog_list/<int:pk>",views.blogpost, name= 'blogpost'),
	# path("blog_list/newpost/",views.newpost, name="newpost"),
	# path("blog_list/<int:pk>/edit/",views.editpost, name= 'editpost')
] 
