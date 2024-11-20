from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView, FormView
from catalog.models import Product, Category
from django.contrib import messages
from django.core.mail import EmailMessage
from catalog.forms.forms import ContactForm, ProductForm, ProductModeratorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.mixins import OwnerOrModeratorRequiredMixin
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """
    Представление главной страницы
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Переопределение метода с использованием кеширования.
        """
        cache_key = 'product_list'  # Уникальный ключ для кеша
        queryset = cache.get(cache_key)  # Попытка получить данные из кеша

        if not queryset:  # Если данные отсутствуют в кеше
            queryset = Product.objects.filter(is_active=True)  # Выполняем запрос
            cache.set(cache_key, queryset, timeout=60 * 15)  # Сохраняем в кеш на 15 минут

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Привязываем текущего пользователя к полю owner
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление страницы товара
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, UpdateView):
    """
    Представление редактирования товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_class(self):
        user = self.request.user

        if user.groups.filter(name='moderators').exists():
            return ProductModeratorForm
        return ProductForm


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    """
    Представление удаления товара
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


class ContactsView(FormView):
    """
    Представление страницы контактов
    """
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contacts')  # Здесь укажи URL для перенаправления после успешной отправки

    def form_valid(self, form):
        """
        Переопределение метода для отправки письма при успешной отправки формы
        """
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        subject = f'Новое сообщение от {name}'
        recipient_list = ['lacryk@gmail.com']

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='lacryk@yandex.ru',
            to=recipient_list,
        )

        email.headers = {
            'Reply-To': 'lacryk@yandex.ru',
        }

        email.send(fail_silently=False)

        messages.success(self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.')  # Добавляем сообщение об успехе
        return super().form_valid(form)  # Вызовем метод родителя для перенаправления на success_url

    def form_invalid(self, form):
        """
        Если форма недействительна, просто отобразим шаблон с ошибками
        """
        return super().form_invalid(form)


class ProductsByCategoryView(ListView):
    """
    Представление для отображения продуктов в определенной категории
    """
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        return get_products_by_category(category)

    def get_context_data(self, **kwargs):
        """
        Добавление категории в контекст для отображения на странице.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = get_object_or_404(Category, id=category_id)
        return context
