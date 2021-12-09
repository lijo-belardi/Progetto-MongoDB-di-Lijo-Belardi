from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

'''
@login_required()
def buy_order_view(request):
    data = Market()
    currency = data.updated_data()

    # Orders lists
    purchase_orders_list = OrderToBuy.objects.filter(status='open').order_by('price')
    sale_orders_list = OrderToSell.objects.filter(status='open').order_by('price')

    if request.method == 'POST':
        print(f'request.POST results:\n{ request.POST }')

        # Buy Order
        form = OrderForm(request.POST or None)
        if form.is_valid():
            status = 'open'
            price = form.cleaned_data.get('price')
            quantity = form.cleaned_data.get('quantity')
            P_Q = price*quantity

            wallet_buyer = Wallet.objects.get(user=request.user)
            if price < 0.0:
                messages.error(request, 'Cannot put a price lower than 0')
                return redirect('app:buy')
            if quantity < 0.0:
                messages.error(request, 'Cannot put a quantity lower than 0')
                return redirect('app:buy')

            if wallet_buyer.usd_wallet >= price and wallet_buyer.btc_wallet >= quantity:
                wallet_buyer.usd_wallet -= price
                wallet_buyer.usd_balance = wallet_buyer.usd_wallet
                wallet_buyer.btc_wallet -= quantity
                wallet_buyer.btc_balance = wallet_buyer.btc_wallet
                wallet_buyer.save()


                # Order creation
                new_buy_order = OrderToBuy.objects.create(user=wallet_buyer,
                                                             status=status,
                                                             price=price,
                                                             quantity=quantity,
                                                             modified=timezone.now())
                # Order matching
                if sale_orders_list.exists():
                    for num, sale_order in enumerate(sale_orders_list):
                        if new_buy_order.user != sale_order.user:

                            if sale_order.price <= new_buy_order.price:
                                messages.success(request, f'Partner found! Purchase Order ID: {new_buy_order._id}.\n'
                                                         f'Sale order id: {sale_order._id}.\n'
                                                 )

                                # Modifying orders.
                                if sale_order.quantity >= new_buy_order.quantity:
                                    # Buy order still open. Updating bitcoins yet to be bought.
                                    actual_btc = new_buy_order.quantity

                                    new_buy_order.quantity += sale_order.quantity
                                    new_buy_order.price -= sale_order.price
                                    new_buy_order.status = 'close'
                                    new_buy_order.save()

                                    wallet_buyer.btc_wallet += new_buy_order.quantity
                                    wallet_buyer.btc_balance = wallet_buyer.btc_wallet
                                    wallet_buyer.usd_wallet += new_buy_order.price
                                    wallet_buyer.usd_balance = wallet_buyer.usd_wallet
                                    wallet_buyer.save()

                                    messages.success(request, f"Buy order id: {new_buy_order._id}. Status: {new_buy_order.status}.\n"
                                                             f"BTC before trade: {actual_btc}; BTC after trade: {new_buy_order.quantity};")


                                    # Sell order can close.
                                    sell_order = OrderToSell.objects.get(_id=sale_order._id)
                                    sell_order.status = "close"
                                    sell_order.save()

                                    messages.success(request, f'Sell order id: {sell_order._id}. received the money successfully. Status: {sell_order.status}.')
                                    messages.success(request, 'Your order has been totally executed! Congratulations!')
                                    return redirect('app:buy')
                                elif sale_order.quantity < new_buy_order.quantity:
                                    messages.error(request, "The amount of bitcoins sold is less than the amount you want to buy\n"
                                                           f"amount of bitcoins placed for sale : {sale_order.quantity} \n"
                                                           f"amount of bitcoins you want to buy : {new_buy_order.quantity}")


                            else:
                                return redirect('app:buy')
                else:
                    messages.success(request, 'Your order is successfully added to the Order Book!')
                    return redirect('app:buy')
            else:
                messages.error(request, 'Your balance is not enough.')
        else:
            messages.error(request, 'Order can not have negative values!')





    # Orders lists refresh
    form = OrderForm()
    profile_pocket = Profile.objects.get(user=request.user)
    # Getting latest trade price

    return render(request, 'app/buy.html', {'form': form,
                                                 'purchase_orders_list': purchase_orders_list,
                                                 'sale_orders_list': sale_orders_list,
                                                 'profile_pocket': profile_pocket,
                                                 'currency': currency
                                                 })
'''