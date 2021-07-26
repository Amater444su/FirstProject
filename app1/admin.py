from django.contrib import admin
from .models import (
    Product,
    Cart,
    Profile,
    Comment,
    WishList,
    EmailMessage,
    Message

)


class CommentAdmin(admin.TabularInline):
    model = Comment


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'text')


class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin, ]
    list_display = ('id', 'name', 'price', 'create_data')
    list_filter = ('price', 'create_data')


class ProductInlinesAdmin(admin.TabularInline):
    model = Product


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number')
    inlines = [ProductInlinesAdmin, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)
admin.site.register(WishList)
admin.site.register(EmailMessage)
admin.site.register(Message, MessageAdmin)

