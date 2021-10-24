from django.http.request import QueryDict
from django.shortcuts import redirect, render
from django import forms

# Create your views here.

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
    print(request.method)
    print(request.GET)
    return render(request, 'qrcode.html')