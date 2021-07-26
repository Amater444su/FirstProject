import ipdb
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.views.generic.edit import FormMixin
# FormMixin с класа генерик, добавляет возможность подключать форму,
# подробнее: (https://github.com/django/django/blob/main/django/views/generic/edit.py)
from .models import Product, ProductType, Cart, Comment, Profile, WishList, Message, EmailMessage
from .forms import ProductForm, CommentForm, UserForm, MessageForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import count_total_product_amount


class ProductListView(ListView):
    """Выводит список всех товаров"""
    # model = Product     # Моя модель ( таблица с БД )
    template_name = 'home.html'  # Сылка как в функции
    context_object_name = 'list_products'  # Контекстк который раньше передавал в функции

    def get_context_data(self, *args, **kwargs):
        """Передает дополнительный контекст
         (список типов, кол-во продуктов)"""
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['list_types'] = ProductType.choices
        try:
            context['Cart'] = Cart.objects.filter(owner=self.request.user).first()
            context['Wishlist'] = WishList.objects.filter(author=self.request.user).first()
        except TypeError:
            pass

        return context

    def get_queryset(self):
        """Фильтрация и Поиск товара"""
        filter_param = self.request.GET.get('type')
        search_param = self.request.GET.get('search')
        if filter_param:
            queryset = Product.objects.filter(type=filter_param)
        elif search_param:
            queryset = Product.objects.filter(name__icontains=search_param)
        else:
            queryset = Product.objects.all()
        return queryset


# def home(request):
#
#     if request.query_params:
#         product_type = request.query_params.get('type')
#         list_product = Product.objects.get(type=product_type)
#     else:
#         list_product = Product.objects.all()
#
#     context = {
#         'list_product': list_product
#
#     }
#     return render(request, 'home.html', context)


class HomeDetailView(DetailView, FormMixin, SuccessMessageMixin):
    """Вывод определенного товара с БД"""
    model = Product
    template_name = 'detail.html'
    context_object_name = 'get_product'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})



# def detail(request, id):

#     """Вывод товара с БД"""
#     get_product = Product.objects.get(id=id)
#     context = {
#         'get_product': get_product
#     }
#     return render(request, 'detail.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара в БД"""
    model = Product
    success_msg = 'Add successful'
    template_name = 'edit_page.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        kwargs['list_product'] = Product.objects.all().order_by('id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save
        return super().form_valid(form)


# def edit_page(request):
#
#     suc = False
#
#     if request.method == 'POST':    # Если в моей html странице form method имеет значние пост
#         form = Productform(request.POST)    # (request.POST) получаем параметры с браузера
#         if form.is_valid():     # Если форма валидна, тоесть все прохидит то идем дальше :)
#             form.save()     # Сохраняем значения юзера
#             suc = True
#
#     context = {
#         'list_product': Product.objects.all().order_by('id'),
#         'form': Productform(),
#         'suc': suc
#
#     }
#     return render(request, 'edit_page.html', context)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление товара в БД"""
    model = Product
    template_name = 'edit_page.html'
    form_class = ProductForm
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     if self.request.user != kwargs['instance'].author:
    #         return self.handle_no_permission()
    #     return kwargs


# def update_page(request, id):
#
#     if request.method == 'POST':    # Если в моей html странице form method имеет значние пост
#         form = Productform(request.POST, instance=Product.objects.get(id=id))    # (request.POST) получаем параметры
#         # с браузера
#         if form.is_valid():     # Если форма валидна, тоесть все проходит то идем дальше :)
#             form.save()     # Сохраняем значения юзера
#
#     context = {
#
#         'get_product': Product.objects.get(id=id),
#         'form': Productform(instance=Product.objects.get(id=id)),
#         'update': True
#     }
#     return render(request, 'edit_page.html', context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')

    # Для работы этого класса необходимо написать форму
    # <form action="{% url 'delete_page' i.id %}" method="post">{% csrf_token %}

    # def delete(self, request, *args, **kwargs):
    #     success_url = reverse_lazy('profile_products')
    #     self.object = self.get_object()
    #     if self.request.user != self.object.author:
    #         return self.handle_no_permission()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)
    #     # return HttpResponse()


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление коментария"""
    model = Comment
    # success_url = '/detail/'

    def get_success_url(self):
        # ipdb.set_trace()
        comment = self.object
        return reverse_lazy('detail', kwargs={'pk': comment.product_id})

    def delete(self, request, *args, **kwargs):
        # ipdb.set_trace()
        self.object = self.get_object()
        success_url = reverse_lazy('detail', kwargs={'pk': self.object.product_id})
        post = Product.objects.filter(author=self.object.product_id).first()
        if self.request.user != self.object.author and self.request.user != post.author:
            return self.handle_no_permission()
        self.object.delete()
        return HttpResponseRedirect(success_url)
        # return HttpResponse()

    # def delete(self, request, *args, **kwargs):
    #     success_url = reverse_lazy('profile_products')
    #     self.object = self.get_object()
    #     if self.request.user != self.object.author:
    #         return self.handle_no_permission()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)
    #     # return HttpResponse()


class ProfileView(ListView):
    """Профиль пользователя"""

    model = Product
    template_name = 'profile.html'
    context_object_name = 'get_product'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['wishlist'] = WishList.objects.filter(author=self.request.user).first()
        return context


class ProfileProductsView(ListView):
    """Товар в профиле пользователя"""

    template_name = 'profile_products.html'
    context_object_name = 'get_product'

    def get_queryset(self):
        queryset = Product.objects.filter(author=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileProductsView, self).get_context_data(*args, **kwargs)
        context['wishlist'] = WishList.objects.filter(author=self.request.user).first()
        return context


class ProfileProductCreateView(CreateView):
    model = Product
    success_msg = 'Add successful'
    template_name = 'profile_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('profile_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save
        return super().form_valid(form)


class CartView(LoginRequiredMixin, View, SuccessMessageMixin):
    """Корзина пользователя"""

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(owner=request.user).first()
        if cart:
            total_products, total_price = count_total_product_amount(request)
            context = {
                'cart': cart,
                'total_price': total_price,
                'total_products': total_products

            }
            return render(request, 'cart.html', context)
        else:
            return render(request, 'cart_empty.html')

    def post(self, request, product_id):
       # ipdb.set_trace()
        user = request.user  # Достали юзера и записали юзера, который сейчас залогинен нас сайт
        product = Product.objects.filter(
            id=product_id).first()  # Достал определенный товар(продукт), с формы получил пк
        # при помощи пк и достал его, так же метод 'first()' возвращает первый елемен
        # user_cart = Cart.objects.filter(owner=user)
        user_cart, created = Cart.objects.get_or_create(  # создаем или берем уже готовую инстанц модель
            owner=user,  # берем если уже создано
            defaults={  # в дефолт записываем, если инстанц модели небыл создан
                # 'products': product,
                'total_products': 1,
                'final_price': product.price
            }
        )

        user_cart.products.add(product)
        return HttpResponseRedirect('/')
        # return render(request, 'cart.html', context)

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Товар успешно добавлен в корзину"
    # get = Выводит данные, не меняя данных!
    # post = Прийнмает новые данные, и созднает новый обьект!


class ProfileUpdateView(UpdateView):
    """Обновление данных пользователя"""
    model = Profile
    form_class = UserForm
    template_name = 'Profile_update.html'
    success_url = reverse_lazy('home')


class ProductDeleteFromCartView(View):
    """Удаление связи корзины и продукта"""

    def get(self, request, pk):
        # ipdb.set_trace()
        user = request.user  # Достали юзера и записали юзера, который сейчас залогинен нас сайт
        product = Product.objects.filter(id=pk).first()
        user_cart = Cart.objects.filter(owner=user).first()
        user_cart.products.remove(product)
        user_cart.save()
        return HttpResponseRedirect('/cart/')


def get_email(request, detail_id):
    """Отправка емейла владельцу товара"""
    # ipdb.set_trace()
    # form = MessageForm()
    action = request.POST['action']
    message = 'qwe'
    if request.method == 'POST' and action == 'make_message':
        message = request.POST['message']
    send_mail('Test subject', message, settings.EMAIL_HOST_USER, ['hikosif724@dmsdmg.com'], fail_silently=False)
    context = {
        # 'form': form
    }
    # return HttpResponseRedirect(reverse('detail', kwargs={'pk': detail_id}))
    return render(request, 'detail.html', context)


class GetEmailView(View):

    def post(self, request, detail_id):
        user = request.user
        product = Message.objects.filter(id=detail_id).first()
        user_message, created = EmailMessage.objects.get_or_create(
            writer=user,
            defaults={
                'to_user': 1,
            }
        )

        user_message.products.add(product)
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': detail_id}))


class WishListView(View):
    """Список желаней пользователя"""

    def get(self, request, *args, **kwargs):
        ipdb.set_trace()
        wishlist = WishList.objects.filter(author=request.user).first()
        context = {
                'wishlist': wishlist,
            }
        return render(request, 'profile.html', context)

    def post(self, request, product_id):
        # ipdb.set_trace()
        user = request.user
        product = Product.objects.filter(id=product_id).first()
        user_wishlist, created = WishList.objects.get_or_create(
            author=user,
            defaults={
                'total_products': 1,
            }
        )

        user_wishlist.products.add(product)
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': product_id}))


class ProductDeleteFromWishListView(View):
    """Удаление связи список желаний и продукта"""

    def get(self, request, pk):
        # ipdb.set_trace()
        user = request.user  # Достали юзера и записали юзера, который сейчас залогинен нас сайт
        product = Product.objects.filter(id=pk).first()
        wishlist = WishList.objects.filter(author=user).first()
        wishlist.products.remove(product)
        wishlist.save()
        return HttpResponseRedirect('/profile/')


class SendMessageView(CreateView):
    """Вывод определенного товара с БД"""
    model = Message
    template_name = 'detail.html'
    context_object_name = 'message'
    form_class = MessageForm
