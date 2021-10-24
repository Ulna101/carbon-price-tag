from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django import forms
from carbon_price_qr.qr_gen import create_qr

# Create your views here.
URL = "carbon-price-tag.herokuapp.com"
class QRCodeRequestForm(forms.Form):
    material = forms.CharField(help_text="Material of the Clothing Item")
    item = forms.CharField(help_text="Clothing item being sold")
    origin = forms.CharField(help_text="Origin of Clothing")
    destination = forms.CharField(help_text="Destination of Clothing")
    
def index(request):
    if request.method == 'POST':
        vars = {k: request.POST[k] for k in ['material', 'item', 'origin', 'destination']}
        post = QueryDict('', mutable=True)
        post.update(vars)
        return redirect('/qr?' + post.urlencode())
    return render(request, 'index.html', {'form': QRCodeRequestForm()})

def qr(request):
    target = URL + "/tag?" + request.GET.urlencode()
    print(request.GET)
    return render(request, 'qrcode.html', {'qr': "data:image/png;base64," + create_qr(target)})