from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_complaint, name='submit-complaint'),
    path('complaints/', views.view_complaints, name='view-complaints'),
    path('complaints/action/<int:complaint_id>/', views.take_action, name='take-action'),
]
