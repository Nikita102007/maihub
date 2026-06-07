from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from mai_hub.forms import AddPostForm, UploadFileForm
from mai_hub.models import MaiHub, Category, TagPost, UploadFiles
from mai_hub.utils import DataMixin


class MaiHubHome(DataMixin, ListView):
    template_name = 'mai_hub/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return MaiHub.published.all().select_related('cat')


def about(request):
    contact_list = MaiHub.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mai_hub/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'mai_hub/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    # permission_required = 'mai_hub.add_maihub'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    model = MaiHub
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'mai_hub/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    # permission_required = 'mai_hub.change_maihub'

    # Ограничиваем выборку объектов только постами текущего пользователя
    def get_queryset(self):
        # Если пользователь суперпользователь, он может редактировать все
        if self.request.user.is_superuser:
            return self.model.objects.all()
        # Иначе - только свои посты
        return self.model.objects.filter(author=self.request.user)

    # Дополнительная проверка на уровне dispatch (если get_queryset не сработал или нужна более строгая проверка)
    def dispatch(self, request, *args, **kwargs):
        # Получаем объект до проверки прав, чтобы убедиться, что он существует
        obj = self.get_object()
        # Если пользователь не автор и не суперпользователь
        if obj.author != request.user and not request.user.is_superuser:
            # Перенаправляем на главную или страницу ошибки 403
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


def contact(request):
    return render(request, "Обратная связь")


def login(request):
    return render(request, "Войти")


class MaiHubCategory(DataMixin, ListView):
    template_name = 'mai_hub/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return MaiHub.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


class ShowPost(DataMixin, DetailView):
    template_name = 'mai_hub/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(MaiHub.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'mai_hub/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return MaiHub.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')