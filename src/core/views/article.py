from src.core.config.main import *

def set_file(request, id):
    dir = "article"
    file_num = request.POST.get("file_num") or 0
    deleted_files = request.POST.get("deleted_files") or "[]"
    for ch in range(int(file_num)):
        type = request.POST.get(f"file_{ch}_type")
        if type == "iframe":
            file_ = request.POST.get(f"file_{ch}")
            file(article_id=id, type="iframe", link=file_, date=get_date()).save()
            continue
        file_ = request.FILES.get(f"file_{ch}")
        ext = request.POST.get(f"file_{ch}_ext")
        name = request.POST.get(f"file_{ch}_name")
        size = request.POST.get(f"file_{ch}_size")
        link = upload_file(dir=dir, file=file_, ext=ext)
        file(article_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
    for ch in json.loads(deleted_files):
        if file.objects.filter(id=ch).exists():
            config = file.objects.get(id=ch)
            remove_file(f"{dir}/{config.link}")
            config.delete()

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].articles: return redirect('/')
    data['articles'] = list(reversed(article.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids:
            article.objects.filter(id=int(id)).delete()
            files = file.objects.filter(article_id=int(id))
            for f in files:
                remove_file(f"article/{f.link}")
                f.delete()
        return JsonResponse({"status": True})
    return render(request, 'article/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].articles: return redirect('/')
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        content = request.POST.get("content")
        notes = request.POST.get("notes")
        active = bool(request.POST.get("active"))
        article(
            title=title, description=description, content=content, notes=notes,
            active=active, date=get_date(),
        ).save()
        id = article.objects.latest("id").id
        set_file(request, id)
        return JsonResponse({"status": True})
    return render(request, 'article/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].articles: return redirect('/')
    if not article.objects.filter(id=id).exists(): return redirect("/articles")
    data['article'] = article.objects.get(id=id)
    files = file.objects.filter(article_id=id)
    data['files'] = [[ch.id, ch.type, f"article/{ch.link}"] for ch in files]
    if request.method == "POST":
        config = article.objects.get(id=id)
        config.title = request.POST.get("title")
        config.description = request.POST.get("description")
        config.content = request.POST.get("content")
        config.notes = request.POST.get("notes")
        config.active = bool(request.POST.get("active"))
        config.save()
        set_file(request, id)
        return JsonResponse({"status": True})
    return render(request, 'article/edit.html', data)
