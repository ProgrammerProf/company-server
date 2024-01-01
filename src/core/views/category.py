from src.core.config.main import *

def set_file(request, old_file=''):
    dir = "category"
    new_file = request.FILES.get('file_0')
    ext = request.POST.get('file_0_ext')
    if new_file:
        if old_file: remove_file(f"{dir}/{old_file}")
        return upload_file(dir=dir, file=new_file, ext=ext)
    return old_file or "default.png"

def data_table(category_id):
    items = list(reversed(product.objects.filter(category_id=category_id, role=1)))
    titles = ['name', 'price', 'date']
    data = []
    for ch in items:
        files = file.objects.filter(product_id=ch.id, type='image')
        image = files[0].link if files else ch.image
        image = f"/static/media/product/{image}"
        data.append([ch.id, f"{image}~{ch.name}", f"{ch.new_price} R.S", ch.date.split(' ')[0]])
    return {'titles': titles, 'data': data}

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].categories: return redirect('/')
    data['categories'] = list(reversed(category.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids:
            category.objects.get(id=int(id)).delete()
            for ch in product.objects.filter(category_id=int(id)):
                ch.category_id = 0
                ch.save()
        return JsonResponse({"status": True})
    return render(request, 'category/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].categories: return redirect('/')
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        products = bool(request.POST.get("allow_products"))
        active = bool(request.POST.get("active"))
        if category.objects.filter(name=name).exists(): return JsonResponse({"status": "name"})
        image = set_file(request)
        category(
            name=name, products=products, description=description,
            active=active, date=get_date(), image=image
        ).save()
        return JsonResponse({"status": True})
    return render(request, 'category/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].categories: return redirect('/')
    if not category.objects.filter(id=id).exists(): return redirect("/categories")
    data['category'] = category.objects.get(id=id)
    data['products'] = product.objects.filter(role=1)
    data['relations'] = data_table(id)
    if request.method == "POST":
        config = category.objects.get(id=id)
        name = request.POST.get("name")
        if category.objects.filter(name=name).exists() and config.name != name:
            return JsonResponse({"status": "name"})
        config.name = request.POST.get("name")
        config.description = request.POST.get("description")
        config.products = bool(request.POST.get("allow_products"))
        config.active = bool(request.POST.get("active"))
        config.image = set_file(request, config.image)
        config.save()
        products = json.loads(request.POST.get("products") or "[]")
        for ch in product.objects.filter(category_id=id, role=1):
            if ch.id not in products:
                ch.category_id = 0
                ch.save()
        for ch in products:
            if product.objects.filter(id=ch, role=1).exists():
                config = product.objects.get(id=ch)
                config.category_id = id
                config.save()
        return JsonResponse({"status": True})
    return render(request, 'category/edit.html', data)
