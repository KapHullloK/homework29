from django.urls import path

from ads import views_category

urlpatterns = [
    path('', views_category.CategoryListView.as_view()),
    path('<int:pk>/', views_category.CategoriesDetailView.as_view()),
    path('create/', views_category.CategoryCreateView.as_view()),
    path('<int:pk>/update/', views_category.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', views_category.CategoryDeleteView.as_view()),
]
