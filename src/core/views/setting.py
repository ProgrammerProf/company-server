from src.core.config.main import *

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].settings: return redirect('/')
    data['setting'] = setting.objects.get(id=1)
    if request.method == "POST":
        if request.headers['request'] == "save_data":
            config = setting.objects.get(id=1)
            config.name = request.POST.get("name") or ""
            config.phone = request.POST.get("phone") or ""
            config.email = request.POST.get("email") or ""
            config.city = request.POST.get("city") or ""
            config.url = request.POST.get("url") or ""
            config.language = request.POST.get("language") or "en"
            config.facebook = request.POST.get("facebook") or ""
            config.whatsapp = request.POST.get("whatsapp") or ""
            config.youtube = request.POST.get("youtube") or ""
            config.instagram = request.POST.get("instagram") or ""
            config.telegram = request.POST.get("telegram") or ""
            config.twetter = request.POST.get("twetter") or ""
            config.linkedin = request.POST.get("linkedin") or ""
            config.save()
        if request.headers['request'] == "save_options":
            config = setting.objects.get(id=1)
            config.theme = request.POST.get("theme")
            config.enable_register = bool(request.POST.get("enable_register"))
            config.enable_login = bool(request.POST.get("enable_login"))
            config.enable_contacts = bool(request.POST.get("enable_contacts"))
            config.enable_orders = bool(request.POST.get("enable_orders"))
            config.enable_chat = bool(request.POST.get("enable_chat"))
            config.enable_chat_files = bool(request.POST.get("enable_chat_files"))
            config.deactive = bool(request.POST.get("deactive"))
            config.save()
        if request.headers['request'] == "deletes":
            btn = request.POST.get("btn")
            if btn == "users": user.objects.filter(role=2).delete()
            if btn == "admins": user.objects.filter(role=1).exclude(super=True).delete()
            if btn == "orders": order.objects.all().delete()
            if btn == "coupons": coupon.objects.all().delete()
            if btn == "contacts": contact.objects.all().delete()
            if btn == "chats":
                friend.objects.all().delete()
                chat.objects.all().delete()
                remove_file("chat")
            if btn == "mails":
                mail.objects.all().delete()
                file.objects.all().exclude(mail_id=0).delete()
                remove_file("mail")
            if btn == "categories":
                config = category.objects.all()
                for ch in config:
                    remove_file(f"category/{config.image}")
                    ch.delete()
            if btn == "products":
                product.objects.all().delete()
                files = file.objects.all().exclude(product_id=0)
                for ch in files:
                    remove_file(f"product/{ch.link}")
                    ch.delete()
            if btn == "articles":
                article.objects.all().delete()
                files = file.objects.all().exclude(article_id=0)
                for ch in files:
                    remove_file(f"article/{ch.link}")
                    ch.delete()
        return JsonResponse({"status": True})
    return render(request, 'setting.html', data)
