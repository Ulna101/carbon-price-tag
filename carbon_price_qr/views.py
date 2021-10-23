from django.shortcuts import render
from input_form import QRCodeRequestForm

# Create your views here.
def index(request):
    context = {}
    context['form'] = QRCodeRequestForm()
    return render(request, 'carbon_price_qr/index.html', context)