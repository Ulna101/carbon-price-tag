from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django import forms
from carbon_price_qr.qr_gen import create_qr
from carbon_price_qr.carbon_cost import carbon_cost

# Create your views here.
URL = "carbon-price-tag.herokuapp.com"
class QRCodeRequestForm(forms.Form):
    material = forms.CharField()
    item = forms.CharField()
    transport = forms.CharField()
    origin = forms.CharField()
    destination = forms.CharField()
    
def index(request):
    if request.method == 'POST':
        vars = {k: request.POST[k].strip().lower() for k in ['material', 'item', 'transport', 'origin', 'destination']}
        post = QueryDict('', mutable=True)
        post.update(vars)
        return redirect('/qr?' + post.urlencode())
    return render(request, 'index.html', {'form': QRCodeRequestForm()})

def qr(request):
    target = URL + "/tag?" + request.GET.urlencode()
    print(request.GET)
    return render(request, 'qrcode.html', {'qr': "data:image/png;base64," + create_qr(target)})

def tag(request):
    params = {}
    params['c_cost'] = carbon_cost(request.GET.dict())
    return render(request, 'tag.html', params)