from django import template
from app.models import *
register = template.Library()

@register.filter()
def parse(value):
    try: return json.loads(value)
    except: ...
    return ""

@register.filter()
def slice(value, length):
    value = str(value or '').replace('\r', ' ').replace('\n', '')
    if len(value) > length: return f"{value[:length]}..."
    return value[:length]

@register.filter()
def split(value, key):
    try: return value.split(key)
    except: ...
    return ''

@register.filter()
def index(value, key):
    try: return value[key]
    except: ...
    return value

@register.filter()
def date(value):
    try: return value.split(" ")[0]
    except: ...
    return value or ''

@register.filter()
def value(value):
    return value if value else ''

@register.filter()
def get_category(value):
    try: return category.objects.get(id=value).name
    except: ...
    return '--'

@register.filter()
def get_product(value):
    try: return product.objects.get(id=value).name
    except: ...
    return ''

@register.filter()
def get_user(value):
    try: return user.objects.get(id=value).name
    except: ...
    return ''

@register.filter()
def product_image(value):
    try:
        files = file.objects.filter(product_id=value, type='image')
        return files[0].link if files else 'default.png'
    except: ...
    return 'default.png'

@register.filter()
def user_image(value):
    try: return user.objects.get(id=value).image
    except: ...
    return 'default.png'

@register.filter()
def article_image(value):
    try:
        files = file.objects.filter(article_id=value, type='image')
        return files[0].link if files else 'default.png'
    except: ...
    return 'default.png'
