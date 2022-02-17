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
    # Updated currency variable
    data = Market()
    currency = data.updated_data()

    # List's creation
    purchase_orders_list = Order.objects.filter(status='open', type='buy').order_by('-price')
    sale_orders_list = Order.objects.filter(status='open', type='sell').order_by('-price')

    # wallet and user's profile variables
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
                    messages.success(request, f'Your  purchase order of {new_buy_order.quantity} BTC for {new_buy_order.price}, {new_buy_order._id}  is successfully added to the Order Book! || Status: {new_buy_order.status}')

                    # Order matching
                    if sale_orders_list.exists():
                        # Checking evey element of "sale_orders_list"
                        for sale_order in sale_orders_list:
                            if sale_order.price <= new_buy_order.price:
                                messages.info(request, f'Search for the best sales order')
                                messages.info(request, f'Partner found! sale order id:{sale_order._id}')
                                messages.success(request, f'He wants to sell {sale_order.quantity} BTC for {sale_order.price} $')
                                messages.info(request, 'Start of the bitcoin exchange')

                                # First case
                                if sale_order.quantity == new_buy_order.quantity:
                                    # Setting actual BTC
                                    actual_btc = profile_wallet.btc_wallet

                                    # Setting status of the new buy order
                                    new_buy_order.quantity = sale_order.quantity
                                    new_buy_order.status = 'close'
                                    new_buy_order.save()

                                    profile_wallet.btc_wallet += new_buy_order.quantity
                                    profile_wallet.usd_wallet -= (sale_order.price * sale_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'Your Buy order id: {new_buy_order._id}. || Status: {new_buy_order.status}.')
                                    messages.success(request, f'|| BTC before exchange: {actual_btc}; || BTC after exchange: {profile_wallet.btc_wallet};')

                                    # Sell order can close.
                                    sell_order = Order.objects.get(_id=sale_order._id)
                                    profile_seller = Wallet.objects.get(user=sell_order.profile)
                                    profile_seller.usd_wallet += (sale_order.price * sale_order.quantity)

                                    profile_seller.save()
                                    sale_order.status = 'close'
                                    sale_order.save()

                                    messages.success(request, f'Sell order id: {sale_order._id}. || Status: {sale_order.status}.')
                                    messages.success(request, f'\nThe User who Sold has Received  successfully {sale_order.price}$ *{sale_order.quantity} .')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app/exchange/order/<int:id>/')

                                # Second case
                                elif sale_order.quantity > new_buy_order.quantity:
                                    # Setting actual BTC
                                    actual_btc = profile_wallet.btc_wallet

                                    new_buy_order.price = sale_order.price
                                    new_buy_order.status = 'close'
                                    new_buy_order.save()

                                    profile_wallet.btc_wallet += new_buy_order.quantity
                                    profile_wallet.usd_wallet -= (new_buy_order.price * new_buy_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'Your Buy order id: {new_buy_order._id}. || Status: {new_buy_order.status}.')
                                    messages.success(request, f'|| BTC before exchange: {actual_btc}; || BTC after exchange: {profile_wallet.btc_amount};')

                                    sale_order.quantity -= new_buy_order.quantity
                                    sale_order.save()

                                    sell_order = Order.objects.get(_id=sale_order._id)
                                    profile_s = Profile.objects.get(user=sell_order.profile.user)
                                    profile_s.usd_wallet += (new_buy_order.price * new_buy_order.quantity)
                                    profile_s.save()

                                    messages.success(request, f'Sell order id: {sale_order._id}. || Status: {sale_order.status}.')
                                    messages.success(request, f'\nThe User who Sold has Received  successfully {new_buy_order.price}$ *{new_buy_order.quantity}.')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app:order')

                                # Third case
                                elif sale_order.quantity < new_buy_order.quantity:
                                    actual_btc = profile_wallet.btc_wallet

                                    new_buy_order.quantity -= sale_order.quantity
                                    new_buy_order.save()

                                    profile_wallet.btc_wallet += sale_order.quantity
                                    profile_wallet.usd_wallet -= (sale_order.price * sale_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'\nYour Buy order id: {new_buy_order._id}. || Status: {new_buy_order.status}.')
                                    messages.success(request, f'\n|| BTC before exchange: {actual_btc}; || BTC after exchange: {profile_wallet.btc_amount};')

                                    sale_order.status = 'close'
                                    sale_order.save()

                                    sell_order = Order.objects.get(_id=sale_order._id)
                                    profile_s = Profile.objects.get(user=sell_order.profile.user)
                                    profile_s.usd_wallet += (sale_order.price * sale_order.quantity)
                                    profile_s.save()

                                    messages.success(request, f'Sell order id: {sale_order._id}. || Status: {sale_order.status}.')
                                    messages.success(request, f'\nThe User who Sold has Received  successfully {sale_order.price} $ * {sale_order.quantity}.')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app:order')

                                # Fourth case
                                else:
                                    return redirect('app:order')
                            return redirect('app:order')
                    else:
                        return redirect('app/exchange/order/<int:id>/')
                else:
                    messages.error(request, 'Your balance is not enough.')
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
                    messages.success(request, f'Your sales order of {new_sell_order.quantity} BTC for {new_sell_order.price}, {new_sell_order._id} is successfully added to the Order Book! || Status:{new_sell_order.status}')

                    # Order matching
                    if purchase_orders_list.exists():
                        # Checking evey element of "purchase_orders_list"
                        for buy_open_order in purchase_orders_list:
                            if buy_open_order.price >= new_sell_order.price:
                                messages.info(request, f'\nSearch for the best purchase order')
                                messages.info(request, f'\nPartner found! purchase order id:{buy_open_order._id}')
                                messages.success(request, f'\nHe wants to buy {buy_open_order.quantity} BTC for {buy_open_order.price} $')
                                messages.info(request, '\nStart of the bitcoin exchange')

                                # First case
                                if buy_open_order.quantity == new_sell_order.quantity:

                                    # Sell order can close.
                                    actual_usd = profile_wallet.usd_wallet
                                    new_sell_order.price = buy_open_order.price
                                    new_sell_order.status = 'close'
                                    new_sell_order.save()

                                    profile_wallet.usd_wallet += (new_sell_order.price * new_sell_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'\nSell order id: {new_sell_order._id}. || Status: {new_sell_order.status}.')
                                    messages.success(request, f'\n|| USD before exchange: {actual_usd}; || USD after exchange: {profile_wallet.usd_amount};')

                                    profile_b = Profile.objects.get(user=buy_open_order.profile.user)
                                    profile_b.btc_wallet += new_sell_order.quantity
                                    profile_b.usd_wallet -= (buy_open_order.price * buy_open_order.quantity)
                                    profile_b.save()

                                    buy_open_order.status = 'close'
                                    buy_open_order.save()

                                    messages.success(request, f'\nBuy order id: {buy_open_order._id}. || Status: {buy_open_order.status}.')
                                    messages.success(request, f'\nThe User who purchased has Received  successfully {new_sell_order.quantity} BTC.')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app:order')

                                # Second case
                                elif buy_open_order.quantity > new_sell_order.quantity:
                                    actual_usd = profile_wallet.usd_wallet

                                    new_sell_order.price = buy_open_order.price
                                    new_sell_order.status = 'close'
                                    new_sell_order.save()

                                    profile_wallet.usd_wallet += (new_sell_order.price * new_sell_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'\nSell order id: {new_sell_order._id}. || Status: {new_sell_order.status}.')
                                    messages.success(request, f'\n|| USD before exchange: {actual_usd}; || USD after exchange: {profile_wallet.usd_amount};')

                                    buy_open_order.quantity -= new_sell_order.quantity
                                    buy_open_order.save()

                                    if buy_open_order.quantity == 0.00:
                                        buy_open_order.status = "close"
                                        buy_open_order.save()

                                    profile_b = Profile.objects.get(user=buy_open_order.profile.user)
                                    profile_b.btc_wallet += new_sell_order.quantity
                                    profile_b.usd_wallet -= (buy_open_order.price * new_sell_order.quantity)
                                    profile_b.save()

                                    messages.success(request, f'Buy order id: {buy_open_order._id}. || Status: {buy_open_order.status}.')
                                    messages.success(request, f'\nThe User who purchased has Received  successfully {new_sell_order.quantity} BTC.')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app:order')

                                # Third case
                                elif buy_open_order.quantity < new_sell_order.quantity:
                                    actual_usd = profile_wallet.usd_wallet
                                    new_sell_order.quantity -= buy_open_order.quantity
                                    new_sell_order.save()

                                    if new_sell_order.quantity == 0.00:
                                        new_sell_order.status = 'close'
                                        new_sell_order.save()

                                    profile_wallet.usd_wallet += (buy_open_order.price * buy_open_order.quantity)
                                    profile_wallet.save()

                                    messages.success(request, f'Sell order id: {new_sell_order._id}. || Status: {new_sell_order.status}.')
                                    messages.success(request, f'\n|| USD before exchange: {actual_usd}; || USD after exchange: {profile_wallet.usd_amount};')

                                    profile_b = Profile.objects.get(user=buy_open_order.profile.user)
                                    profile_b.btc_wallet += buy_open_order.quantity
                                    profile_b.usd_wallet -= (buy_open_order.price * buy_open_order.quantity)
                                    profile_b.save()

                                    buy_open_order.status = 'close'
                                    buy_open_order.save()
                                    messages.success(request, f'Buy order id: {buy_open_order._id}. || Status: {buy_open_order.status}.')
                                    messages.success(request, f'\nThe User who purchased has Received  successfully {buy_open_order.quantity} BTC.')
                                    messages.info(request, f'\nThe bitcoin exchange has been totally executed! Congratulations!')
                                    return redirect('app:order')

                                # Fourth case
                                else:
                                    return redirect('app:order')
                        return redirect('app:order')
                    else:
                        return redirect('app:order')
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