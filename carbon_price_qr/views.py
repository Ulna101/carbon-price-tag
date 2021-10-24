from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django import forms
from carbon_price_qr.qr_gen import create_qr
from carbon_price_qr.carbon_cost import *

# Create your views here.
URL = "carbon-price-tag.herokuapp.com"
choices = data_headings()
class QRCodeRequestForm(forms.Form):
    material = forms.ChoiceField(choices=choices['material'])
    item = forms.ChoiceField(choices=choices['item'])
    transport = forms.ChoiceField(choices=choices['transport'])
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
    return render(request, 'qrcode.html', {'qr': "data:image/png;base64," + create_qr(target)})

def tag(request):
    params = {}
    req = request.GET.dict()
    params['inp'] = req
    params['c_cost'] = carbon_cost(req)
    params['c_avg'] = avarage_cost(req['item'])
    params['dist'] = round(calculate_distance(req['origin'], req['destination']))
    params['transport_cost'] = round(get_method(req['transport']), 5)
    params['item_cost'] = round(get_carbon(req['item'], req['material']))
    return render(request, 'tag.html', params)