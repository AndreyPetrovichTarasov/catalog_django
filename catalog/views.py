from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView, FormView
from catalog.models import Product
from django.contrib import messages
from django.core.mail import send_mail
from .templates.forms.forms import ContactForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contacts')  # Здесь укажи URL для перенаправления после успешной отправки

    def form_valid(self, form):
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']

        # send_mail(
        #     subject=f'Новое сообщение от {name}',
        #     message=message,
        #     from_email='your_email@gmail.com',
        #     recipient_list=['recipient_email@example.com'],
        # )

        messages.success(self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.')  # Добавляем сообщение об успехе
        return super().form_valid(form)  # Вызовем метод родителя для перенаправления на success_url

    def form_invalid(self, form):
        # Если форма недействительна, просто отобразим шаблон с ошибками
        return super().form_invalid(form)
