from src.core.config.main import *

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].contacts: return redirect('/')
    data['contacts'] = list(reversed(contact.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids: contact.objects.get(id=int(id)).delete()
        return JsonResponse({"status": True})
    return render(request, 'contact.html', data)
