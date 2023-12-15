
from . import views
from django.urls import path, re_path
from .views import poll_detail, edit_profile, delete_profile, register, login_view, logout_view, vote, create_poll

app_name = 'polls'
urlpatterns = [
    path('catalog/', views.IndexView.as_view(), name='index'),
    path('polls/', views.PollsView.as_view(), name='polls_views'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

]
