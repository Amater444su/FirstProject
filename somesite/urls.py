from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.ProductListView.as_view(), name='home'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='detail'),
    path('profile/detail/<int:pk>', views.ProductDetailView.as_view(), name='detail_profile'),
    path('edit-page/', views.ProductCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', views.ProductUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', views.ProductDeleteView.as_view(), name='delete_page'),
    path('comment-delete/<int:pk>', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('profile/', views.ProfileView.as_view(), name='profile_page'),
    path('profile/products/', views.ProfileProductsView.as_view(), name='profile_products'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('products/<int:product_id>/add_to_cart', views.CartView.as_view(), name='add_to_cart'),
    path('profile_update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile_create/', views.ProfileProductCreateView.as_view(), name='profile_create'),
    path('cart/<int:pk>', views.ProductDeleteFromCartView.as_view(), name='cart_delete'),
    # path('email/<int:pk>/<int:product_id>', views.get_email, name='email'),
    path('products/<int:product_id>/wishlist', views.WishListView.as_view(), name='add_to_wishlist'),
    path('wishlist/<int:pk>', views.ProductDeleteFromWishListView.as_view(), name='wishlist_delete'),
    # path('message/<int:pk>', views.SendMessageView.as_view(), name='get_message'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
