
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.conf import settings

def save_pdf(params:dict):
    
    template = get_template("pdf.html")

    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name = uuid.uuid4()

    try:
        with open(str(settings.BASE_DIR) + f'/public/static/{file_name}.pdf','wb+')as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),output)

    except Exception as e:
        print(e)

    if pdf.err:
        return '',False

    return file_name,True

import random
from django.core.cache import cache


def send_otp_mobile(mobile, user_obj):

    if cache.get(mobile):
        return False,cache.ttl(mobile)

    try:

        otp_to_sent = random.randint(1000,9999)
        cache.set(mobile, otp_to_sent, timeout=60)
        user_obj.otp = otp_to_sent
        user_obj.save()
        return True, 0

    except Exception as e:
        print(e)