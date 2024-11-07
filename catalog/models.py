from django.db import models


class Category(models.Model):
    """
    Определение модели Категории
    """
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Product(models.Model):
    """
    Определение модели товара
    """
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    descriptions = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/products/", blank=True, null=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Укажите, доступен ли продукт для продажи."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}. Категория: {self.category}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "category", "price"]