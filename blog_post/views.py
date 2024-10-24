from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, FormView
from django.views.generic.edit import CreateView, UpdateView

from blog_post.models import BlogPost
from .templates.forms.forms import ContactForm


class ArticleListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-views_count')


class ArticleCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:home')


class ArticleDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
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
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/article_form.html'
    # success_url = reverse_lazy('blog:home')

    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:home')


# class ContactsView(FormView):
#     template_name = 'blog/contacts.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('blog:contacts')  # Здесь укажи URL для перенаправления после успешной отправки
#
#     def form_valid(self, form):
#         name = form.cleaned_data['name']
#         message = form.cleaned_data['message']
#         subject = f'Новое сообщение от {name}'
#         recipient_list = ['lacryk@gmail.com']
#
#         email = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email='lacry@rambler.ru',
#             to=recipient_list,
#         )
#
#         # Добавление заголовков
#         email.headers = {
#             'Reply-To': 'lacry@rambler.ru',
#         }
#
#         # email.send(fail_silently=False)
#
#         messages.success(self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.')  # Добавляем сообщение об успехе
#         return super().form_valid(form)  # Вызовем метод родителя для перенаправления на success_url
#
#     def form_invalid(self, form):
#         # Если форма недействительна, просто отобразим шаблон с ошибками
#         return super().form_invalid(form)