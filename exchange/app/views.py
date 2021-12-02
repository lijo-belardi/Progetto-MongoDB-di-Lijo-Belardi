from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PublishOrderToBuy

@login_required()
def homepage_view(request):
    return render(request, "homepage.html")

def publish_order_to_buy(request):
    ...
