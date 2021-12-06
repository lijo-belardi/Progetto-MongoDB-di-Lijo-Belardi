from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PublishOrderToBuy
from .market import Market

@login_required()
def homepage_view(request):
    data = Market()
    currency = data.updated_data()
    return render(request, "homepage.html", {"currency": currency})





def publish_order_to_buy(request):
    ...
