from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView, FormView
from catalog.models import Product
from django.contrib import messages
from django.core.mail import EmailMessage
from .templates.forms.forms import ContactForm


class ProductListView(ListView):
    """
    Представление главной страницы
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    """
    Представление создания товара
    """
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductDetailView(DetailView):
    """
    Представление страницы товара
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    """
    Представление редактирования товара
    """
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductDeleteView(DeleteView):
    """
    Представление удаления товара
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')


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
            from_email='lacry@rambler.ru',
            to=recipient_list,
        )

        email.headers = {
            'Reply-To': 'lacry@rambler.ru',
        }

        email.send(fail_silently=False)

        messages.success(self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.')  # Добавляем сообщение об успехе
        return super().form_valid(form)  # Вызовем метод родителя для перенаправления на success_url

    def form_invalid(self, form):
        """
        Если форма недействительна, просто отобразим шаблон с ошибками
        """
        return super().form_invalid(form)
