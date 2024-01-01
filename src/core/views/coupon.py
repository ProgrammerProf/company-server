from src.core.config.main import *

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].coupons: return redirect('/')
    data['coupons'] = list(reversed(coupon.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids: coupon.objects.get(id=int(id)).delete()
        return JsonResponse({"status": True})
    return render(request, 'coupon.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].coupons: return redirect('/')
    if request.method == "POST":
        code = request.POST.get("code")
        discount = request.POST.get("discount")
        if coupon.objects.filter(code=code).exists():
            return JsonResponse({"status": "code"})
        coupon(code=code, discount=discount, date=get_date()).save()
    return JsonResponse({"status": True})
