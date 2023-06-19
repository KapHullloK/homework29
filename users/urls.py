from django.urls import path

from users import user_views

urlpatterns = [
    path('', user_views.UserListView.as_view()),
    path('<int:pk>/', user_views.UserDetailView.as_view()),
    path('create/', user_views.UserCreateView.as_view()),
    path('<int:pk>/update/', user_views.UserUpdateView.as_view()),
    path('<int:pk>/delete/', user_views.UserDeleteView.as_view()),
]
