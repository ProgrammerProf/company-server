from src.core.config.main import *

def get_contacts(user_id):
    contacts = friend.objects.all()
    contacts = contacts.order_by('update')
    data = []
    for ch in contacts:
        if user.objects.filter(id=ch.person_1, active=True).exists():
            person_id = ch.person_1
            if ch.remove_2: continue
        elif user.objects.filter(id=ch.person_2, active=True).exists():
            person_id = ch.person_2
            if ch.remove_1: continue
        else: continue
        user_data = user.objects.get(id=person_id)
        msg_data = []
        chats = chat.objects.filter(
            Q(receiver=person_id, remove_sender=False) |
            Q(sender=person_id, remove_receiver=False)
        )
        for sw in chats:
            msg_data.append({
                "id": sw.id, "date": sw.date, "type": sw.type, "content": sw.content, "link": sw.link,
                "name": sw.name, "size": sw.size, "sender": sw.sender, "active": sw.see_receiver,
            })
        data.append({
            "id": ch.id, "contact_id": user_data.id, "friend_date": ch.date,
            "name": user_data.name, "image": user_data.image, "messages": msg_data
        })
    return data

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].chat: return redirect('/')
    curr_user = session(request)
    data['users'] = list(reversed(user.objects.filter(active=True, role=2)))
    if request.method == "POST":
        if request.headers["request"] == "get_contacts":
            contacts = json.dumps(get_contacts(session(request)))
            return JsonResponse({"status": True, "contacts": contacts})
        if request.headers["request"] == "new_contact":
            user_id = int(request.POST.get("id"))
            if not user.objects.filter(id=user_id, active=True).exists():
                return JsonResponse({"status": False})
            if friend.objects.filter(person_1=session(request), person_2=user_id).exists():
                config = friend.objects.get(person_1=session(request), person_2=user_id)
                config.remove_1 = False
                config.update = get_date()
                config.save()
            elif friend.objects.filter(person_2=session(request), person_1=user_id).exists():
                config = friend.objects.get(person_2=session(request), person_1=user_id)
                config.remove_2 = False
                config.update = get_date()
                config.save()
            else:
                friend(
                    person_1=session(request), person_2=user_id, date=get_date(),
                    update=get_date()
                ).save()
                config = friend.objects.latest('id')
            user_data = user.objects.get(id=user_id)
            data = {
                "status": True, "id": config.id, "online": False,
                "name": user_data.name, "image": user_data.image, "msgs": []
            }
            return JsonResponse(data)
        if request.headers["request"] == "delete_contact":
            id = int(request.POST.get("id"))
            for_all = bool(request.POST.get("all"))
            if not friend.objects.filter(id=id).exists():
                return JsonResponse({"status": False})
            config = friend.objects.get(id=id)
            if config.person_1 == curr_user: config.remove_1 = True
            else: config.remove_2 = True
            config.save()
            chats = chat.objects.filter(
                Q(sender=config.person_1, receiver=config.person_2) |
                Q(sender=config.person_2, receiver=config.person_1)
            )
            if (config.remove_1 and config.remove_2) or for_all:
                for ch in chats:
                    remove_file(f"chat/{ch.link}")
                    ch.delete()
                config.delete()
            else:
                for ch in chats:
                    if ch.sender == curr_user: ch.remove_sender = True
                    else: ch.remove_receiver = True
                    ch.save()
            return JsonResponse({"status": True})
        if request.headers["request"] == "active_chat":
            user_id = int(request.POST.get("id"))
            chats = chat.objects.filter(sender=user_id)
            for ch in chats:
                ch.see_receiver = True
                ch.save()
            return JsonResponse({"status": True})
        if request.headers["request"] == "send_message":
            user_id = int(request.POST.get("user_id"))
            if not user.objects.filter(id=user_id, active=True).exists():
                return JsonResponse({"status": False})
            relation = friend.objects.filter(Q(person_2=user_id) | Q(person_1=user_id))
            if not relation.exists(): return JsonResponse({"status": False})
            content = request.POST.get("content")
            type = request.POST.get("type")
            link = request.POST.get("link")
            name = request.POST.get("name")
            size = request.POST.get("size")
            ext = request.POST.get("ext")
            date = get_date()
            if type == "video" or type == "image" or type == "file":
                file_ = request.FILES.get("file")
                link = upload_file(dir='chat', file=file_, ext=ext)
            chat(
                content=content, type=type, link=link, name=name, size=size, date=date,
                receiver=user_id, sender=curr_user, see_sender=True
            ).save()
            for ch in relation:
                ch.update = get_date()
                ch.save()
            msg_id = chat.objects.latest("id").id
            data = {
                "status": True, "id": msg_id, "link": link, "name": name, "type": type, "size": size,
                "ext": ext, "date": date, "content": content, "user_id": user_id, "admin_id": curr_user,
                "sender": curr_user, "active": True
            }
            return JsonResponse(data)
    return render(request, 'chat.html', data)
