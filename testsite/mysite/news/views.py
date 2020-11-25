from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages

from .models import News, Category
from .forms import NewsForm, UserRegisterForm
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Успешная регистрация')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
        messages.add_message(request, messages.INFO, 'Отказ!')
    return render(request, 'news/register.html', {'form': form})

def login(request):
    return render(request, 'news/login.html')

def test(request):
    objects = ['User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'user7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    # стиль пагинации описан в базовом шаблоне base.html
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    # extra_context = {'title': 'Главная '}
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Главная страница'
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/new/news_detail.html'
    # pk_url_kwarg = 'news_id'

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    login_url = '/admin/' # если не авторизован - на страницу регистрации
    # raise_exception = True # если не авторизован - ошибка 403

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, template_name='news/category.html', context={'news': news, 'category': category})

class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).\
            select_related('category')

# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, template_name='news/view_news.html', context={'news_item': news_item})

#
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, template_name='news/add_news.html', context={'form': form})
