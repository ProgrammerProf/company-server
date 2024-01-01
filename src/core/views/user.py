from src.core.config.main import *

def set_file(request, old_file=''):
    dir = "user"
    new_file = request.FILES.get('file_0')
    ext = request.POST.get('file_0_ext')
    if new_file:
        if old_file: remove_file(f"{dir}/{old_file}")
        return upload_file(dir=dir, file=new_file, ext=ext)
    return old_file or "default.png"

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].users: return redirect('/')
    data['users'] = list(reversed(user.objects.filter(role=2, super=False)))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids:
            remove_file(f"user/{user.objects.get(id=int(id)).image}")
            user.objects.get(id=int(id)).delete()
            order.objects.filter(user_id=int(id)).delete()
        return JsonResponse({"status": True})
    return render(request, 'user/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].users: return redirect('/')
    if request.method == "POST":
        email = request.POST.get("email")
        if user.objects.filter(email=email).exists():
            return JsonResponse({"status": "email"})
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        password = request.POST.get("password")
        notes = request.POST.get("notes")
        age = float(request.POST.get("age"))
        chat = bool(request.POST.get("chat"))
        contacts = bool(request.POST.get("contacts"))
        active = bool(request.POST.get("active"))
        image = set_file(request)
        user(
            name=name, email=email, phone=phone, city=city, password=password,
            image=image, age=age, active=active, date=get_date(), notes=notes,
            ip=client(request, 'ip'), host=client(request, 'host'), role=2, chat=chat, contacts=contacts
        ).save()
        return JsonResponse({"status": True})
    return render(request, 'user/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].users: return redirect('/')
    if not user.objects.filter(id=id, role=2).exists(): return redirect("/users")
    data['item'] = user.objects.get(id=id)
    if request.method == "POST":
        config = user.objects.get(id=id)
        email = request.POST.get("email")
        if user.objects.filter(email=email).exists() and config.email != email:
            return JsonResponse({"status": "email"})
        config.name = request.POST.get("name")
        config.email = request.POST.get("email")
        config.phone = request.POST.get("phone")
        config.city = request.POST.get("city")
        config.password = request.POST.get("password")
        config.notes = request.POST.get("notes")
        config.age = float(request.POST.get("age"))
        config.chat = bool(request.POST.get("chat"))
        config.contacts = bool(request.POST.get("contacts"))
        config.active = bool(request.POST.get("active"))
        config.image = set_file(request, config.image)
        config.save()
        return JsonResponse({"status": True})
    return render(request, 'user/edit.html', data)
