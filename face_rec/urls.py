from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name='home'),
	path("add_employee/",views.register_employee,name= 'register_employee'),
	path("add_employee/train",views.train, name= 'train'),
	# path("blog_list/newpost/",views.newpost, name="newpost"),
	# path("blog_list/<int:pk>/edit/",views.editpost, name= 'editpost')
] 
