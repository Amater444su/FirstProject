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
    profile_image = models.ImageField(default='static/static_images/in.jpg', upload_to='images_profile/', null=True, blank=True,
                                      verbose_name='Картинка')


class ProductType(models.TextChoices):
    SNEAKERS = 'Кросовки'
    GUMSHOES = 'Кеды'
    CLOGS = 'Сабо'
    CROCS = 'Кроги'
    EARTH_SHOES = 'Легкие кросовки'
    MOCCASINS = 'Мокасины'
    SANDLAS = 'Сандали'
    SLIPPERS = 'Тапки'
    OXFORDS = 'Оксофорды'
    HIGH_HEELS = 'Туфли на каблуке'


class Product(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    create_data = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    name = models.CharField(max_length=30, verbose_name='Имя')
    text = models.TextField()
    price = models.IntegerField(null=True, verbose_name='Цена')
    image = models.ImageField(default='static/static_images/no.png', upload_to='static_images/', null=True, blank=True,
                              verbose_name='Картинка')
    type = models.CharField(choices=ProductType.choices, max_length=40)  # 'choices' передаю свой класс 'ProductType'

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


