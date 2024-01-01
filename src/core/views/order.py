from src.core.config.main import *

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    data['orders'] = list(reversed(order.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids: order.objects.get(id=int(id)).delete()
        return JsonResponse({"status": True})
    return render(request, 'order/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    data['products'] = list(reversed(product.objects.all()))
    data['users'] = list(reversed(user.objects.filter(role=2)))
    data['coupons'] = list(reversed(coupon.objects.all()))
    if request.method == "POST":
        user_id = integer(request.POST.get("user"))
        product_id = integer(request.POST.get("product"))
        coupon_id = integer(request.POST.get("coupon"))
        if not product.objects.filter(id=product_id).exists():
            return JsonResponse({"status": False})
        coupon_name = ''
        discount = 0
        price = product.objects.get(id=product_id).price
        if coupon.objects.filter(id=coupon_id).exists():
            cp = coupon.objects.get(id=coupon_id)
            coupon_name = cp.code
            discount = cp.discount * price / 100
            price -= discount
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        notes = request.POST.get("notes")
        paid = bool(request.POST.get("paid"))
        sent = bool(request.POST.get("sent"))
        active = bool(request.POST.get("active"))
        order(
            user_id=user_id, product_id=product_id, coupon=coupon_name, discount=discount,
            price=price, date=get_date(), paid=paid, sent=sent, name=name, email=email, phone=phone,
            address=address, notes=notes, active=active
        ).save()
        return JsonResponse({"status": True})
    return render(request, 'order/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    if not order.objects.filter(id=id).exists(): return redirect("/orders")
    data['order'] = order.objects.get(id=id)
    data['products'] = list(reversed(product.objects.all()))
    data['users'] = list(reversed(user.objects.filter(role=2)))
    data['coupons'] = list(reversed(coupon.objects.all()))
    if request.method == "POST":
        config = order.objects.get(id=id)
        config.name = request.POST.get("name")
        config.email = request.POST.get("email")
        config.phone = request.POST.get("phone")
        config.address = request.POST.get("address")
        config.notes = request.POST.get("notes")
        config.paid = bool(request.POST.get("paid"))
        config.sent = bool(request.POST.get("sent"))
        config.active = bool(request.POST.get("active"))
        config.save()
        return JsonResponse({"status": True})
    return render(request, 'order/edit.html', data)
