from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_acts/', views.generate_acts, name='generate_acts'),
    path('generate_orders/', views.generate_orders, name='generate_orders'),
    path('generate_document_package/', views.generate_document_package, name='generate_document_package'),
    path('dashboard/profile/', views.user_profile, name='user_profile'),
    path('dashboard/documents/', views.documents, name='documents'),
    path('dashboard/new-request/', views.new_request, name='new_request'),
    path('dashboard/tasks/', views.tasks, name='tasks'),
    path('edit_document/<int:document_id>/', views.edit_document, name='edit_document'),
    path('dashboard/support/', views.support, name='support'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('fill_template/<int:template_id>/', views.fill_template, name='fill_template'),
    path('delete_template/<int:template_id>/', views.delete_template, name='delete_template'),

]
