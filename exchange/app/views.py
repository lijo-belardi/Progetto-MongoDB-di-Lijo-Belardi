from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# From this app
from .models import Profile, Wallet, Order
from .forms import OrderForm
from .market import Market
# Other apps import

# Other imports


@login_required()
def homepage_view(request):
    data = Market()
    currency = data.updated_data()
    return render(request, "homepage.html", {"currency": currency})


@login_required()
def order_view(request, id):
    data = Market()
    currency = data.updated_data()
    purchase_orders_list = Order.objects.filter(status='open', type='buy').order_by('-price')
    sale_orders_list = Order.objects.filter(status='open', type='sell').order_by('-price')
    wallet = get_object_or_404(Wallet, user_id=id)
    user_profile = get_object_or_404(Profile, user_id=id)
    # Orders lists
    if request.method == 'POST':
        if request.POST.get('buy'):

            # Buy Order
            form = OrderForm(request.POST or None)
            if form.is_valid():
                status = 'open'
                type = 'buy'
                price = form.cleaned_data.get('price')
                quantity = form.cleaned_data.get('quantity')
                profile_wallet = Wallet.objects.get(user=request.user)

                if price <= 0.0:
                    messages.error(request, 'Cannot put a price lower than 0')
                    return redirect('app:order')
                if quantity <= 0.0:
                    messages.error(request, 'Cannot put a quantity lower than 0')
                    return redirect('app:order')

                if profile_wallet.usd_wallet >= price:
                    # Order creation
                    new_buy_order = Order.objects.create(profile=request.user,
                                                         status=status,
                                                         type=type,
                                                         price=price,
                                                         quantity=quantity,
                                                         modified=timezone.now())
                    messages.success(request,
                                     f'Your  purchase order of {new_buy_order.quantity} BTC for {new_buy_order.price}, {new_buy_order._id}  is successfully added to the Order Book! || Status: {new_buy_order.status}')
            else:
                messages.error(request, 'Order can not have negative values!')

        elif request.POST.get('sell'):

            # sell order
            form = OrderForm(request.POST or None)
            if form.is_valid():
                type = 'sell'
                status = 'open'
                price = form.cleaned_data.get('price')
                quantity = form.cleaned_data.get('quantity')
                profile_wallet = Wallet.objects.get(user=request.user)

                if price <= 0.0:
                    messages.error(request, 'Cannot put a price lower than 0')
                    return redirect('app:order')
                if quantity <= 0.0:
                    messages.error(request, 'Cannot put a quantity lower than 0')
                    return redirect('app:order')

                if profile_wallet.btc_wallet >= quantity:
                    profile_wallet.btc_wallet -= quantity
                    profile_wallet.save()
                    # Order creation
                    new_sell_order = Order.objects.create(profile=request.user,
                                                          type=type,
                                                          status=status,
                                                          price=price,
                                                          quantity=quantity,
                                                          modified=timezone.now())
                    messages.success(request,
                                     f'Your sales order of {new_sell_order.quantity} BTC for {new_sell_order.price}, {new_sell_order._id} is successfully added to the Order Book! || Status:{new_sell_order.status}')
                else:
                    messages.error(request, 'Your balance is not enough.')
            else:
                messages.error(request, 'Order can not have negative values!')
    form = OrderForm()
    return render(request, "order.html", {"currency": currency,
                                          "wallet": wallet,
                                          "user_profile": user_profile,
                                          "form": form,
                                          "purchase_orders_list": purchase_orders_list,
                                          "sale_orders_list": sale_orders_list})