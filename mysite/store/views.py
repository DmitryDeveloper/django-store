from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, loader
from django.urls import reverse
from .models import Category, Product, Order, ProductOrder
from .services.BucketManager import BucketManager
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, OrderFrom
from django.db.models import Q
from django.core.mail import mail_managers


def register(request):
    data = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        data['form'] = form
        if form.is_valid():
            form.save()
            data['res'] = "New account created, please login"
            return HttpResponseRedirect('/accounts/login/')
        else:
            data['res'] = "Failed"
            return render(request, 'store/register.html', data)
    else:
        form = RegisterForm()
        data['form'] = form
        return render(request, 'store/register.html', data)


# CATEGORIES AND PRODUCRS LOGIC


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    bucket_manager = BucketManager(request)
    user_bucket_data_count = bucket_manager.count_of_product()
    context = {'categories': categories, 'products': products, 'user_bucket_data_count': user_bucket_data_count}
    return render(request, 'store/category/index.html', context)


def show_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    bucket_manager = BucketManager(request)
    user_bucket_data_count = bucket_manager.count_of_product()
    return render(request, 'store/category/detail.html',
                  {'category': category, 'user_bucket_data_count': user_bucket_data_count})


def show_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bucket_manager = BucketManager(request)
    user_bucket_data_count = bucket_manager.count_of_product()
    context = {'product': product, 'user_bucket_data_count': user_bucket_data_count}
    return render(request, 'store/product/detail.html', context)


# BUCKET LOGIC


def bucket_view(request):
    bucket_manager = BucketManager(request)
    products = bucket_manager.get_products()
    total_price = bucket_manager.get_total_price(products)

    order_message = None
    if 'order_message' in request.GET:
        order_message = request.GET['order_message']
    user_bucket_data_count = bucket_manager.count_of_product()
    context = {
        'products': products,
        'total_price': total_price,
        'user_bucket_data_count': user_bucket_data_count,
        'order_message': order_message
    }
    return render(request, 'store/bucket/index.html', context)


def bucket_store(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bucket_manager = BucketManager(request)
    bucket_manager.add_product_id(product_id)

    redirect_to = None
    if 'redirect_to' in request.POST:
        redirect_to = request.POST['redirect_to']

    if redirect_to == 'product-detail':
        return HttpResponseRedirect(reverse('store:product-detail', kwargs={'product_id': product_id}))
    elif redirect_to == 'bucket':
        return HttpResponseRedirect(reverse('store:bucket-view'))
    else:
        return HttpResponseRedirect(reverse('store:detail', kwargs={'category_id': product.category_id}))


def bucket_reduce(request, product_id):
    bucket_manager = BucketManager(request)
    product_ids = bucket_manager.get_bucket_data()
    product_ids.remove(product_id)
    bucket_manager.set_bucket_data(product_ids)
    return HttpResponseRedirect(reverse('store:bucket-view'))


def bucket_clear(request):
    bucket_manager = BucketManager(request)
    bucket_manager.clear_bucket_data()
    return HttpResponseRedirect(reverse('store:bucket-view'))


# ORDER LOGIC


def make_order(request):
    error_message = None
    if 'error_message' in request.GET:
        error_message = request.GET['error_message']

    bucket_manager = BucketManager(request)
    user_bucket_data_count = bucket_manager.count_of_product()
    context = {'user_bucket_data_count': user_bucket_data_count, 'error_message': error_message}
    return render(request, 'store/order/new-order.html', context)


def order(request):
    city = request.POST['city']
    street = request.POST['street']
    building = request.POST['building']
    flat = request.POST['flat']
    phone = request.POST['phone']

    form = OrderFrom(request.POST)
    if form.is_valid():
        bucket_manager = BucketManager(request)
        total_price = bucket_manager.get_total_price()

        order = Order(
            city=city,
            street=street,
            building=building,
            flat=flat,
            phone=phone,
            status='PR',
            total_price=total_price,
            user_id=request.user.id,
            ip_address=bucket_manager.get_client_ip(request)
        )
        order.save()

        list_product_ids = bucket_manager.get_bucket_data()
        for product_id in list_product_ids:
            product_order = ProductOrder(product_id=product_id, order_id=order.id)
            product_order.save()

        bucket_manager.clear_bucket_data()
        mail_managers(
            'New order was made',
            'Check please admin account, new order was made.',
            fail_silently=False
        )

        redirect_url = reverse('store:bucket-view') + '?order_message=Order made successfully'
    else:
        redirect_url = reverse('store:make-order') + '?error_message=Form data are incorrect'

    return HttpResponseRedirect(redirect_url)


@login_required
def track_orders(request):
    bucket_manager = BucketManager(request)
    orders = Order.objects.filter(Q(user_id=request.user.id) | Q(ip_address=bucket_manager.get_client_ip(request)))
    completed_orders = orders.filter(status='CP')
    active_orders = orders.filter(~Q(status='CP'))

    if 'status' in request.GET and request.GET['status'] == 'completed':
        display_orders = completed_orders
    else:
        display_orders = active_orders

    completed_orders_count = completed_orders.count()
    active_orders_count = active_orders.count()

    user_bucket_data_count = bucket_manager.count_of_product()
    for order in orders:
        product_ids = ProductOrder.objects.filter(order_id=order.id).values_list('product_id', flat=True)
        order.products = Product.objects.filter(id__in=product_ids)
        for product in order.products:
            product.count = product_ids.filter(product_id=product.id).count()

    return render(request, 'store/order/track.html',
                  {'orders': display_orders,
                   'user_bucket_data_count': user_bucket_data_count,
                   'completed_orders_count': completed_orders_count,
                   'active_orders_count': active_orders_count})
