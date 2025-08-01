from django.urls import path,include
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('',views.core_page,name='corepage'),
    path('settings/',views.settings,name='settings'),
    path('login/',LoginView.as_view(template_name ='registration/login.html'), name='login'),
    path('register/', views.SignUp_view, name='register'),
    path('profilepage/', views.profile_view, name='user'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.custom_change_password, name='password_change'),
    path('complain/',views.complain,name='complain'),
    # email conformation code 
    path('activate/<uid64>/<token>/', views.activate_account,name='activate'),

    # for the alert 
    path('emergency/',views.emergency_alert, name='emergency-alert'),
    path('emergency-click/', views.show_emergency_button, name='emergency-button'),
    path('alerts/', views.emergency_alerts_list, name='emergency-alerts-list'),


]
