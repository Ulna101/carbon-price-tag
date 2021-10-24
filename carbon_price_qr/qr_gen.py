import qrcode
import os
from PIL import Image
from io import BytesIO 
from django.templatetags.static import static
from qrcode.image.styledpil import StyledPilImage
import base64

def create_qr(dest):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size = 10,
        border=3
    )
    qr.add_data(dest)
    qr.make(fit=True)
    module_dir = os.path.dirname(__file__)
    img = qr.make_image(fill_color=(83, 132, 63), back_color="white")
    qr_size, _ = img.size
    
    logo_size = int(qr_size * 0.30)
    min = int((qr_size / 2) - (logo_size / 2))
    max = int((qr_size / 2) + (logo_size / 2))
    
    module_dir = os.path.dirname(__file__)
    logo = Image.open(module_dir + '/static/logo.png')
    logo = logo.resize((max - min, max - min))
    
    img.paste(logo, (min, min, max, max))
    
    img_str = BytesIO()
    img.save(img_str, format="PNG")
    img_str = base64.b64encode(img_str.getvalue())
    
    return img_str.decode('ascii')
