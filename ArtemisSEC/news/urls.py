from django.urls import path
from .views import NewsListView, NewsDetailView, NewsCreateView, GetNewsView, DeleteNewsView, NewsListAPIView

urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('news/', NewsCreateView.as_view(), name='create_news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/api/get/<int:news_id>/', GetNewsView.as_view(), name='get_news'),
    path('news/api/delete/<int:news_id>/', DeleteNewsView.as_view(), name='delete_news'),
    path('news/api/list/', NewsListAPIView.as_view(), name='news_list_api'),
]