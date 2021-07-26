from django.test import TestCase

# Create your tests here.

# from django.db import models
#
#
# class ProductType(models.TextChoices):
#     name = 'Кросовки'   # Создаю класс 'ProductType', класс выбора, в нем я обьявляю свои переменные (Теги
#      = 'Кеды'   # по которым я буду сортировать/фильтровать), название с большой буквы
#     # этот класс нужно передать в CharField моей основной модели ( в моем случае 'Product' )
#
#     class Meta:
#         ordering = [
#
#         ]
#
# class Product(models.Model):
#     create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Время в живую поскольку параметр Тру
#     name = models.CharField(max_length=30, verbose_name='Имя')  # Максимальна длина строки
#     text = models.TextField()   # Тест ( много текста ) в отличии от 'CharField' Который принимает определенное
#     # кол-то текста, 'TextField' принимет инфинити текста.
#     price = models.IntegerField(null=True, verbose_name='Цена')
#     image = models.ImageField(default='images/no.png', upload_to='images/', null=True, blank=True, verbose_name='Картинка')
#     # null=True означет что в базе данных может
#     # быть пустое место, может и не быть картинки, blank=True в запросте на бэкенд может не приходить.
#     type = models.ForeignKey('ProductType', null=True, on_delete=models.PROTECT, verbose_name='Категория')
#     #PROTECT = если я удалю тип(связь) то моя модель ( Кверисет ) останеться
#     #CASCADE = если я удалю свою свзять (тип) то модель ( кверисет ) тоже удалиться
#     #type = models.CharField(choices=ProductType.choices, max_length=30)     # 'choices' передаю свой класс 'ProductType'
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = [
#             '-create_data',
#             'price'
#         ]

# from django.db import models
#
#
# class ProductType(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')   # Создаю класс 'ProductType', класс выбора, в нем я обьявляю свои переменные (Теги
#     # по которым я буду сортировать/фильтровать), название с большой буквы
#     # этот класс нужно передать в CharField моей основной модели ( в моем случае 'Product' )
#
#     class Meta:
#         ordering = [
#             'name'
#         ]
#
#     def __str__(self):
#         return 'Категория' + self.name
#
#
# class Product(models.Model):
#     create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Время в живую поскольку параметр Тру
#     name = models.CharField(max_length=30, verbose_name='Имя')  # Максимальна длина строки
#     text = models.TextField()   # Тест ( много текста ) в отличии от 'CharField' Который принимает определенное
#     # кол-то текста, 'TextField' принимет инфинити текста.
#     price = models.IntegerField(null=True, verbose_name='Цена')
#     image = models.ImageField(default='images/no.png', upload_to='images/', null=True, blank=True, verbose_name='Картинка')
#     # null=True означет что в базе данных может
#     # быть пустое место, может и не быть картинки, blank=True в запросте на бэкенд может не приходить.
#     type = models.ForeignKey('ProductType', null=True, on_delete=models.PROTECT, verbose_name='Категория')
#     #PROTECT = если я удалю тип(связь) то моя модель ( Кверисет ) останеться
#     #CASCADE = если я удалю свою свзять (тип) то модель ( кверисет ) тоже удалиться
#     #type = models.CharField(choices=ProductType.choices, max_length=30)     # 'choices' передаю свой класс 'ProductType'
#
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = [
#             '-create_data',
#             'price'
#         ]
