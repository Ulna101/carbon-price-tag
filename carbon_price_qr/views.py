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
    params['c_cost'] = round(carbon_cost(req))
    params['total_transport'] = round(calculate_distance(req['origin'], req['destination']) * 
                            get_method(req['transport']))
    params['c_avg'] = round(avarage_cost(req['item']) + params['total_transport'])
    params['dist'] = round(calculate_distance(req['origin'], req['destination']))
    params['transport_cost'] = round(get_method(req['transport']), 5)
    params['item_cost'] = round(get_carbon(req['item'], req['material']))
    params['equiv'] = get_equivalencies(params['c_cost'])
    params['comps'] = [
        "A wool {} emits {}lbs".format(req['item'], round(get_carbon(req['item'], "wool"))),
        "A cotton {} emits {}lbs".format(req['item'], round(get_carbon(req['item'], "cotton"))),
        "A polyester {} emits {}lbs".format(req['item'], round(get_carbon(req['item'], "polyester"))),
    ]
    return render(request, 'tag.html', params)