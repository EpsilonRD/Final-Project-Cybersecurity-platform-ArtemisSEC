from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import News
from .forms import NewsForm

# View for the main page
class NewsListView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']  # Sort by descending date

# View for the details of the news
class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

# View for creating and editing news (authenticated users only)
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/create_news.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_news'] = News.objects.filter(author=self.request.user).order_by('-created_at')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        news_id = self.request.POST.get('news_id')
        if news_id:
            try:
                existing_news = News.objects.get(pk=news_id, author=self.request.user)
                existing_news.title = form.instance.title
                existing_news.content = form.instance.content
                if self.request.FILES.get('image'):
                    existing_news.image = form.instance.image
                existing_news.save()
                return redirect(self.success_url)
            except News.DoesNotExist:
                form.add_error(None, "News not found or you lack permission to edit it.")
                return self.form_invalid(form)
        return super().form_valid(form)

# API view to fetch news data for editing
class GetNewsView(LoginRequiredMixin, View):
    def get(self, request, news_id, *args, **kwargs):
        try:
            news = News.objects.get(pk=news_id, author=request.user)
            return JsonResponse({
                'success': True,
                'news': {
                    'title': news.title,
                    'content': news.content,
                }
            })
        except News.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'News not found'}, status=404)

# View to delete a news post
class DeleteNewsView(LoginRequiredMixin, View):
    def post(self, request, news_id, *args, **kwargs):
        try:
            news = News.objects.get(pk=news_id, author=request.user)
            news.delete()
            return JsonResponse({'success': True})
        except News.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'News not found'}, status=404)

# API view to fetch the latest news list
class NewsListAPIView(View):
    def get(self, request, *args, **kwargs):
        news_list = News.objects.all().order_by('-created_at')
        news_data = [
            {
                'id': news.pk,
                'title': news.title,
                'content': news.content[:150], 
                'author': news.author.username,
                'created_at': news.created_at.strftime('%d %b %Y %H:%M'),
                'image': news.image.url if news.image else None,
            }
            for news in news_list
        ]
        return JsonResponse({'news_list': news_data})