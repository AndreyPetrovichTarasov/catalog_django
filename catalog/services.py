from catalog.models import Product


def get_products_by_category(category):
    """
    Возвращает список всех активных продуктов в указанной категории.
    :param category: Объект категории или его идентификатор.
    :return: QuerySet с продуктами.
    """
    return Product.objects.filter(category=category, is_active=True)
