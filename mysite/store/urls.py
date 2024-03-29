from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>', views.show_category, name='detail'),
    path('product/<int:product_id>', views.show_product, name='product-detail'),
    path('bucket/', views.bucket_view, name='bucket-view'),
    path('add-to-bucket/<int:product_id>', views.bucket_store, name='bucket-store'),
    path('bucket-reduce/<int:product_id>', views.bucket_reduce, name='bucket-reduce'),
    path('bucket-clear/', views.bucket_clear, name='bucket-clear'),
    path('order/', views.order, name='order'),
    path('make-order/', views.make_order, name='make-order'),
    path('orders/track', views.track_orders, name='track-orders'),
    path('register/', views.register, name='register'),
]
