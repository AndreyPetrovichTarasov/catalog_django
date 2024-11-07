from PIL import Image
from django import forms

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    message = forms.CharField(widget=forms.Textarea, label='Ваше сообщение')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Стилизация каждого поля
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Bootstrap-класс для текстовых полей
                'placeholder': f'Введите {field.label.lower()}'
            })
        self.fields['is_active'].widget = forms.CheckboxInput()

    def clean_name(self):
        """Валидация названия продукта."""
        name = self.cleaned_data.get('name', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f'Название содержит запрещённое слово: {word}')
        return self.cleaned_data['name']

    def clean_descriptions(self):
        """Валидация описания продукта."""
        description = self.cleaned_data.get('descriptions', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f'Описание содержит запрещённое слово: {word}')
        return self.cleaned_data['descriptions']

    def clean_price(self):
        """Валидация стоимости продукта."""
        price = self.cleaned_data.get('price')
        if int(price) < 0:
            raise forms.ValidationError(f'Стоимость товара не может быть отрицательной')
        return self.cleaned_data['price']

    def clean_image(self):
        """Валидация загружаемого изображения."""
        image = self.cleaned_data.get('image')

        if image:
            # Проверяем, что файл имеет корректное расширение
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Файл должен быть с расширением .jpeg, .jpg или .png.')

            # Проверяем формат изображения
            try:
                img = Image.open(image)
                if img.format.upper() not in ['JPEG', 'JPG', 'PNG']:
                    raise forms.ValidationError('Файл должен быть в формате JPEG или PNG.')
            except (IOError, ValueError):
                raise forms.ValidationError('Невозможно открыть изображение. Проверьте файл.')

            # Проверяем размер файла
            max_file_size = 5 * 1024 * 1024  # 5 MB
            if image.size > max_file_size:
                raise forms.ValidationError('Размер файла не должен превышать 5 МБ.')

        return image
