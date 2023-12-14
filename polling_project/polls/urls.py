# polls/urls.py

from django.urls import path, re_path
from .views import index, poll_detail, edit_profile, delete_profile, register, login_view, logout_view, vote

app_name = 'polls'
urlpatterns = [
    path('', index, name='index'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:poll_id>/vote/', vote, name='vote'),
]
