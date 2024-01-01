from app.models import *

def mail_config(product_id):
    settings = setting.objects.filter(id=1).first()
    config = product.objects.filter(id=product_id).first()
    users = user.objects.filter(role=2, active=True)
    if not config or not users or not settings: return
    data = {
        'host': 'https://www.taibet-alkhair.com',
        'img_url': 'https://taibetalkhair.pythonanywhere.com',
        'year': get_date('year'),
        'product': config,
        'settings': settings,
    }
    html_content = render_to_string('mail/news.html', data)
    msg = EmailMultiAlternatives(
        settings.name, strip_tags(html_content), users[0].email,
        [ch.email for ch in users]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_email(product_id):
    threading.Thread(target=mail_config, args=(product_id,)).start()

def set_session(request, id):
    request.session['user'] = id
    request.session['active_user'] = True

def del_session(request):
    try: del request.session['user']
    except: ...
    try: del request.session['active_user']
    except: ...

def del_active(request):
    try: del request.session['active_user']
    except: ...

def session(request):
    id = request.session.get("user")
    if user.objects.filter(id=id, active=True).exists():
        return int(id)
    del_session(request)
    return 0

def active(request):
    return request.session.get("active_user")

def authentication(func):
    @csrf_exempt
    def wrapper(request, *args, **kwargs):
        if not session(request): return redirect('/login')
        if not active(request): return redirect('/lock-screen')
        return func(request, *args, **kwargs)
    return wrapper

def start_data(request):
    logged_user = user.objects.get(id=session(request))
    data = {'user': logged_user}
    return data

def default():
    try:
        if user.objects.filter(super=True).exists(): return
        user(
            name="Super Admin", email="super@gmail.com", password="super123", super=True,
            date=get_date(), chat=True, mail=True, users=True, contacts=True, categories=True,
            products=True, orders=True, articles=True, statistics=True, settings=True, auctions=True
        ).save()
        setting(name="Website").save()
    except: ...

default()
