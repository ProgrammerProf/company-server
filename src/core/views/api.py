from src.core.config.api import *

@csrf_exempt
def default_data(request):
    if request.method == "POST": return JsonResponse(default())
    return JsonResponse({"status": False})

@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if user.objects.filter(email=email).exists():
            return JsonResponse({"status": "exists"})
        user(
            name=email.split("@")[0], email=email, ip=client(request, 'ip'),
            host=client(request, 'host'), role=2, city=client(request, 'country'), date=get_date(),
        ).save()
        user_id = user.objects.latest("id").id
        return JsonResponse({"status": True, "user_id": user_id})
    return JsonResponse({"status": False})

@csrf_exempt
def booking(request):
    if request.method == "POST":
        product_id = integer(request.POST.get("product"))
        config = product.objects.filter(id=product_id).first()
        if not config: return JsonResponse({"status": False})
        if not config.allow_bookings: return JsonResponse({"status": False})
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        notes = request.POST.get("notes")
        price = config.new_price
        order(
            product_id=product_id, name=name, phone=phone, email=email, notes=notes,
            address=client(request, 'city'), date=get_date(), price=price
        ).save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

@csrf_exempt
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        contact(
            name=name, phone=phone, email=email, message=message,
            ip=client(request, 'ip'), host=client(request, 'host'),
            city=client(request, 'city'), date=get_date(),
        ).save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

@csrf_exempt
def category_data(request):
    if request.method == "POST":
        id = integer(request.POST.get('id'))
        return JsonResponse({'data': categories(id), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def product_data(request):
    if request.method == "POST":
        id = integer(request.POST.get("id"))
        details = product_details(id)
        return JsonResponse({'data': details[0], 'recommeded': details[1],**default()})
    return JsonResponse({"status": False})

@csrf_exempt
def auctions(request):
    if request.method == "POST":
        return JsonResponse({'data': products(role=2), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def all_blogs(request):
    if request.method == "POST":
        return JsonResponse({'data': blogs(), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def blog_data(request):
    if request.method == "POST":
        id = integer(request.POST.get("id"))
        return JsonResponse({'data': blog_details(id), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        user_id = integer(request.POST.get("user"))
        if not user.objects.filter(id=user_id, active=True).exists():
            if user.objects.filter(id=user_id, active=False).exists():
                return JsonResponse({"status": False})
            user(name='--', email='--', phone='--', role=3, date=get_date()).save()
            user_id = user.objects.latest("id").id
        if not friend.objects.filter(Q(person_1=user_id) | Q(person_2=user_id)).exists():
            friend(person_1=user_id, date=get_date(), update=get_date()).save()
        content = request.POST.get("content")
        type = request.POST.get("type")
        link = request.POST.get("link")
        name = request.POST.get("name")
        size = request.POST.get("size")
        ext = request.POST.get("ext")
        date = get_date()
        if type == "video" or type == "image" or type == "file":
            file = request.FILES.get("file")
            link = upload_file(dir='chat', file=file, ext=ext)
        chat(
            content=content, type=type, link=link, name=name,
            size=size, date=date, sender=user_id, see_sender=True
        ).save()
        config = friend.objects.filter(Q(person_1=user_id) | Q(person_2=user_id)).first()
        config.update = get_date()
        config.save()
        message = {
            "id": chat.objects.latest("id").id, "link": link, "name": name,
            "type": type, "size": size, "ext": ext, "date": date, "content": content,
            "who_send": "user", "active": False
        }
        return JsonResponse({"status": True, "user_id": user_id, "message": message})
    return JsonResponse({"status": False})

@csrf_exempt
def active_messages(request):
    if request.method == "POST":
        user_id = integer(request.POST.get("user"))
        if user_id:
            for ch in chat.objects.filter(receiver=user_id):
                ch.see_receiver = True
                ch.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

@csrf_exempt
def get_messages(request):
    if request.method == "POST":
        user_id = integer(request.POST.get("user"))
        if not user_id: return JsonResponse({"status": False})
        data = chat.objects.filter(
            Q(sender=user_id, remove_sender=False) |
            Q(receiver=user_id, remove_receiver=False)
        )
        messages = []
        for ch in data:
            messages.append({
                "id": ch.id,
                "content": ch.content, "date": ch.date, "sender": ch.sender,
                "type": ch.type, "link": f"/static/media/chat/{ch.link}", "name": ch.name,
                "size": ch.size, "active": ch.see_receiver
            })
        return JsonResponse({"status": True, "messages": messages})
    return JsonResponse({"status": False})
