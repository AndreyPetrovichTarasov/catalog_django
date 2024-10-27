from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from blog_post.models import BlogPost


class ArticleListView(ListView):
    """
    Представление главной страницы
    """
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """
        Переопределение метода для вывода статей опубликованных и сортированных по просмотрам
        """
        return BlogPost.objects.filter(is_published=True).order_by('-views_count')


class ArticleCreateView(CreateView):
    """
    Представление создания статьи
    """
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:home')


class ArticleDetailView(DetailView):
    """
    Представление страницы статьи
    """
    model = BlogPost
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        """
        Переопределение метода для реализации счётчика просмотров и отправки пиьсма при достижении 100 просмотров
        """
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])

        if obj.views_count == 100:
            email = EmailMessage(
                subject=f'Сообщение о 100 просмотрах: "{obj.title}"',
                body=f'Поздравляю! Ваша статья "{obj.title}" набрала 100 просмотров!',
                from_email='lacry@rambler.ru',
                to=['lacryk@gmail.com'],
            )
            email.headers = {
                'Reply-To': 'lacry@rambler.ru',
            }
            email.send(fail_silently=False)

        return obj


class ArticleUpdateView(UpdateView):
    """
    Представление редактирования статьи
    """
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/article_form.html'
    # success_url = reverse_lazy('blog:home')

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse('blog:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    """
    Представление удаления статьи
    """
    model = BlogPost
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
