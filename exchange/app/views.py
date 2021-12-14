from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# From this app
from .models import Profile, Wallet, OrderToBuy, OrderToSell
from .forms import OrderForm
from .market import Market
# Other apps import

# Other imports


@login_required()
def homepage_view(request):
    data = Market()
    currency = data.updated_data()
    return render(request, "homepage.html", {"currency": currency})


def sell_order_view(request, id):
    wallet = get_object_or_404(Wallet, user_id=id)

    return render(request, "app/sell.html", {"wallet": wallet})


def buy_order_view(request, id):
    wallet = get_object_or_404(Wallet, user_id=id)
    buy_orders_list = OrderToBuy.objects.filter(status='open').order_by('created')
    sell_orders_list = OrderToSell.objects.filter(status='open').order_by('created')

    if request.method == 'POST':

        print(f'request.POST results:\n{request.POST}')
        # Buy Order
        form = OrderForm(request.POST or None)
        if form.is_valid():
            status = 'open'
            price = form.cleaned_data.get('price')
            quantity = form.cleaned_data.get('quantity')

            profile_wallet = Wallet.objects.get(user=request.user)

            if price < 0.0:
                messages.error(request, 'Cannot put a price lower than 0')
                return redirect('app:buy')
            if quantity < 0.0:
                messages.error(request, 'Cannot put a quantity lower than 0')
                return redirect('app:buy')
            if profile_wallet.usd_wallet >= price and profile_wallet.btc_wallet >= quantity:
                profile_wallet.usd_wallet -= price
                profile_wallet.save()
                # Order creation
                new_buy_order = OrderToBuy.objects.create(user=request.user,
                                                             status=status,
                                                             price=price,
                                                             quantity=quantity,
                                                             modified=timezone.now())

                messages.success(request,
                                 f'Your  purchase order of {new_buy_order.quantity} BTC for {new_buy_order.price}  is successfully added to the Order Book! || Status: {new_buy_order.status}')
        else:
            messages.error(request, 'Order can not have negative values!')

    form = OrderForm()
    return render(request, "app/buy.html", {"wallet": wallet, "form": form, "buy_orders_list": buy_orders_list, "sell_orders_list": sell_orders_list})

