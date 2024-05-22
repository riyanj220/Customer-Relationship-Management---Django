from django.urls import path
from . import views
from .views import HomeView ,RegisterView ,CustomLoginView , DashboardView ,RecordCreateView,RecordUpdateView ,RecordDetailView 


urlpatterns=[

    path('', HomeView.as_view(),name= ''),
    path('register',RegisterView.as_view() ,name= 'register'),
    path('login', CustomLoginView.as_view(),name= 'login'), 
    path('dashboard', DashboardView.as_view(),name= 'dashboard'), 
    path('logout', views.logout,name= 'logout'), 
    path('create_record', RecordCreateView.as_view(),name= 'create_record'), 
    path('update_record/<int:pk>', RecordUpdateView.as_view(),name= 'update_record'), 
    path('view_record/<int:pk>', RecordDetailView.as_view(),name= 'view_record'), 
    path('delete_record/<int:pk>', views.delete_record,name= 'delete_record'), 

]