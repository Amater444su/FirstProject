from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Profile(AbstractUser):
    address = models.CharField(max_length=40, blank=True, null=True, verbose_name='Адресс')
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Номер телефона', validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    profile_image = models.ImageField(default='images/in.jpg', upload_to='images_profile/', null=True, blank=True,
                                      verbose_name='Картинка')


class ProductType(models.TextChoices):
    SNEAKERS = 'Кросовки'  # Создаю класс 'ProductType', класс выбора, в нем я обьявляю свои переменные (Теги
    GUMSHOES = 'Кеды'  # по которым я буду сортировать/фильтровать), название с большой буквы
    CLOGS = 'Сабо'
    CROCS = 'Кроги'
    EARTH_SHOES = 'Легкие кросовки'
    MOCCASINS = 'Мокасины'
    SANDLAS = 'Сандали'
    SLIPPERS = 'Тапки'
    OXFORDS = 'Оксофорды'
    HIGH_HEELS = 'Туфли на каблуке'
    # этот класс нужно передать в CharField моей основной модели ( в моем случае 'Product' )


class Product(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    create_data = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')  # Время в живую поскольку параметр Тру
    name = models.CharField(max_length=30, verbose_name='Имя')  # Максимальна длина строки
    text = models.TextField()  # Тест ( много текста ) в отличии от 'CharField' Который принимает определенное
    # кол-то текста, 'TextField' принимет инфинити текста.
    price = models.IntegerField(null=True, verbose_name='Цена')
    image = models.ImageField(default='images/no.png', upload_to='images/', null=True, blank=True,
                              verbose_name='Картинка')
    type = models.CharField(choices=ProductType.choices, max_length=40)  # 'choices' передаю свой класс 'ProductType'

    # null=True означет что в базе данных может
    # быть пустое место, может и не быть картинки, blank=True в запросте на бэкенд может не приходить.
    # type = models.ForeignKey('ProductType', null=True, on_delete=models.PROTECT, verbose_name='Категория')
    # PROTECT = если я удалю тип(связь) то моя модель ( Кверисет ) останеться
    # CASCADE = если я удалю свою свзять (тип) то модель ( кверисет ) тоже удалиться

    def __str__(self):
        return self.name

    class Meta:
        pass


class Cart(models.Model):
    owner = models.ForeignKey(Profile, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='product_comment')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст комента')


class WishList(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Product, blank=True, related_name='wishlist_rel')
    total_products = models.PositiveIntegerField(default=0)


class Message(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор сообщения',
                               related_name='writer_mes')
    topic = models.CharField(max_length=40, blank=True, null=True, verbose_name='Тема сообщения')
    text = models.TextField(blank=True, null=True, verbose_name='Текст сообщения')
    email = models.EmailField(verbose_name='Емейл', blank=True)


class EmailMessage(models.Model):
    author = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='Автор сообщения',
                                  related_name='sender')
    messages = models.ManyToManyField(Message, verbose_name='Сообщения', related_name='messages_rel')