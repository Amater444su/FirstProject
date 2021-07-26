import ipdb
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.views.generic.edit import FormMixin
from .models import Product, ProductType, Cart, Comment, Profile, WishList, Message
from .forms import ProductForm, CommentForm, UserForm, MessageForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import count_total_product_amount


class ProductListView(ListView):
    """Выводит список всех товаров"""
    template_name = 'home.html'
    context_object_name = 'list_products'

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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление товара в БД"""
    model = Product
    template_name = 'edit_page.html'
    form_class = ProductForm
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление коментария"""
    model = Comment

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
        user = request.user
        product = Product.objects.filter(
            id=product_id).first()
        user_cart, created = Cart.objects.get_or_create(
            owner=user,
            defaults={
                'total_products': 1,
                'final_price': product.price
            }
        )

        user_cart.products.add(product)
        return HttpResponseRedirect('/')


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
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


def get_email(request, pk):
    """Отправка емейла владельцу товара"""
    # ipdb.set_trace()
    message = Message.objects.filter(id=pk+1).first()

    send_mail(str(message.topic), str(message.text), settings.EMAIL_HOST_USER, ['hikosif724@dmsdmg.com'],
              fail_silently=False)

    return HttpResponseRedirect('/')


class WishListView(LoginRequiredMixin, View):
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


class ProductDeleteFromWishListView(LoginRequiredMixin, View):
    """Удаление связи список желаний и продукта"""

    def get(self, request, pk):
        # ipdb.set_trace()
        user = request.user
        product = Product.objects.filter(id=pk).first()
        wishlist = WishList.objects.filter(author=user).first()
        wishlist.products.remove(product)
        wishlist.save()
        return HttpResponseRedirect('/profile/')


class SendMessageView(LoginRequiredMixin, CreateView):
    """Cоздание сообщения"""
    # ipdb.set_trace()
    model = Message
    template_name = 'Message.html'
    context_object_name = 'message'
    message = Message.objects.last()
    form_class = MessageForm
    success_url = reverse_lazy('email', kwargs={'pk': message.id})


    def form_valid(self, form):
        #ipdb.set_trace()
        user = Profile.objects.filter(id=self.request.user.id).first()
        self.object = form.save(commit=False)
        self.object.writer = self.request.user
        self.object.email = user.email
        self.object.save
        return super().form_valid(form)
