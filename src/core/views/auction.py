from src.core.config.main import *

def set_file(request, id):
    dir = "product"
    file_num = request.POST.get("file_num") or 0
    deleted_files = request.POST.get("deleted_files") or "[]"
    for ch in range(int(file_num)):
        type = request.POST.get(f"file_{ch}_type")
        if type == "iframe":
            file_ = request.POST.get(f"file_{ch}")
            file(product_id=id, type="iframe", link=file_, date=get_date()).save()
            continue
        file_ = request.FILES.get(f"file_{ch}")
        ext = request.POST.get(f"file_{ch}_ext")
        name = request.POST.get(f"file_{ch}_name")
        size = request.POST.get(f"file_{ch}_size")
        link = upload_file(dir=dir, file=file_, ext=ext)
        file(product_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
    for ch in json.loads(deleted_files):
        if file.objects.filter(id=ch).exists():
            config = file.objects.get(id=ch)
            remove_file(f"{dir}/{config.link}")
            config.delete()

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].auctions: return redirect('/')
    data['products'] = list(reversed(product.objects.filter(role=2)))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids:
            product.objects.filter(id=int(id)).delete()
            order.objects.filter(product_id=int(id)).delete()
            files = file.objects.filter(product_id=int(id))
            for f in files:
                remove_file(f"product/{f.link}")
                f.delete()
        return JsonResponse({"status": True})
    return render(request, 'auction/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].auctions: return redirect('/')
    if request.method == "POST":
        name = request.POST.get("name")
        keys = request.POST.get("keys")
        location = request.POST.get("location")
        company = request.POST.get("company")
        phone = request.POST.get("phone")
        number = request.POST.get("number")
        brochure_url = request.POST.get("brochure_url")
        study_url = request.POST.get("study_url")
        expire_date = request.POST.get("expire_date")
        new_price = float(request.POST.get("new_price"))
        old_price = float(request.POST.get("old_price"))
        included = request.POST.get("included")
        overview = request.POST.get("overview")
        notes = request.POST.get("notes")
        active = bool(request.POST.get("active"))
        allow_bookings = bool(request.POST.get("allow_bookings"))
        product(
            name=name, notes=notes, new_price=new_price, old_price=old_price, location=location,
            active=active, date=get_date(), company=company, keys=keys, role=2,
            phone=phone, number=number, overview=overview, included=included,
            expire_date=expire_date, allow_bookings=allow_bookings, brochure_url=brochure_url,
            study_url=study_url
        ).save()
        id = product.objects.latest("id").id
        set_file(request, id)
        send_email(id)
        return JsonResponse({"status": True})
    return render(request, 'auction/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].auctions: return redirect('/')
    if not product.objects.filter(id=id, role=2).exists(): return redirect("/auctions")
    data['product'] = product.objects.get(id=id, role=2)
    files = file.objects.filter(product_id=id)
    data['files'] = [[ch.id, ch.type, f"product/{ch.link}"] for ch in files]
    if request.method == "POST":
        config = product.objects.get(id=id)
        config.name = request.POST.get("name")
        config.keys = request.POST.get("keys")
        config.location = request.POST.get("location")
        config.company = request.POST.get("company")
        config.phone = request.POST.get("phone")
        config.number = request.POST.get("number")
        config.brochure_url = request.POST.get("brochure_url")
        config.study_url = request.POST.get("study_url")
        config.expire_date = request.POST.get("expire_date")
        config.new_price = float(request.POST.get("new_price"))
        config.old_price = float(request.POST.get("old_price"))
        config.included = request.POST.get("included")
        config.overview = request.POST.get("overview")
        config.notes = request.POST.get("notes")
        config.allow_bookings = bool(request.POST.get("allow_bookings"))
        config.active = bool(request.POST.get("active"))
        config.save()
        set_file(request, id)
        return JsonResponse({"status": True})
    return render(request, 'auction/edit.html', data)
