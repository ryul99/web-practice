from django.urls import path
from api import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('verify_session/', views.verify_session, name='verify_session'),
    path('post/<int:post_id>/comment/', views.comment, name='comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/', views.post_list, name='post_list'),
    path('comment/<int:comment_id>/', views.comment_detail, name='comment_detail'),
]