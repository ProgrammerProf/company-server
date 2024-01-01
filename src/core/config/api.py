from app.models import *

def settings():
    data = setting.objects.filter(id=1).first()
    if not data: return False
    data = {
        "name": data.name, "email": data.email, "phone": data.phone, "city": data.city,
        "facebook": data.facebook, "whatsapp": data.whatsapp, "youtube": data.youtube,
        "twetter": data.twetter, "telegram": data.telegram, "instagram": data.instagram,
        "linkedin": data.linkedin, "theme": data.theme, "image": data.image, "contact": data.enable_contacts,
        "chat": data.enable_chat, "chat_files": data.enable_chat_files, "bookings": data.enable_orders,
        "deactive": data.deactive, "login": data.enable_login, "register": data.enable_register,
        "language": data.language, "active": not data.deactive
    }
    return data

def product_list(data):
    files = file.objects.filter(product_id=data.id)
    images = [[ch.type, f"/static/media/product/{ch.link}"] for ch in files if ch.type == "image"]
    videos = [[ch.type, f"/static/media/product/{ch.link}"] for ch in files if ch.type == "video"]
    iframes = [[ch.type, ch.link] for ch in files if ch.type == "iframe"]
    images = iframes + videos + images
    if not images: images = ['image', f"/static/media/product/{data.image}"]
    list_data = {
        'id': data.id, 'name': data.name, 'location': data.location, "phone": data.phone,
        'new_price': data.new_price, 'old_price': data.old_price, 'views': data.views,
        "reviews": data.reviews, "number": data.number,
        "allow_bookings": data.allow_bookings, 'images': images, "date": data.date,
        'included': json.loads(data.included), 'overview': data.overview,
        "expire_date": data.expire_date, "company": data.company, "study_url": data.study_url,
        'is_market': data.role == 2, "brochure_url": data.brochure_url,
    }
    return list_data

def blog_list(data):
    files = file.objects.filter(article_id=data.id)
    images = [[ch.type, f"/static/media/article/{ch.link}"] for ch in files if ch.type == "image"]
    videos = [[ch.type, f"/static/media/article/{ch.link}"] for ch in files if ch.type == "video"]
    iframes = [[ch.type, ch.link] for ch in files if ch.type == "iframe"]
    images = iframes + videos + images
    if not images: images = ['image', f"/static/media/article/{data.image}"]
    list_data = {
        'id': data.id, 'title': data.title, 'views': data.views, 'likes': data.likes,
        'images': images, "date": data.date, 'content': data.content,
        "description": data.description,
    }
    return list_data

def categories(id=0):
    data = []
    if id: result = category.objects.filter(id=id, active=True)
    else: result = list(reversed(category.objects.filter(active=True)))
    for ch in result:
        products = product.objects.filter(category_id=ch.id, role=1, active=True)
        products = [product_list(sw) for sw in products]
        data.append({
            'id': ch.id, 'name': ch.name, 'description': ch.description,
            'image': f'/static/media/category/{ch.image}',
            'products': json.dumps(products)
        })
    if id: return data[0] if data else False
    return data

def products(role=1, limit=0, excluded=0):
    data = list(reversed(product.objects.filter(role=role, active=True).exclude(id=excluded)))
    if limit: data = data[:limit]
    return [product_list(ch) for ch in data]

def product_details(id=0):
    data = product.objects.filter(id=id, active=True).first()
    if not data: return False
    data.views += 1
    data.save()

    category_id = product.objects.filter(id=id).first().category_id
    same_products = list(reversed(product.objects.filter(category_id=category_id, role=data.role, active=True).exclude(id=id)))[:10]
    if data.role == 2:
        same_products = list(reversed(product.objects.filter(role=2, active=True).exclude(id=id)))[:10]
    recommended = [product_list(ch) for ch in same_products]
    if len(recommended) < 10 and data.role == 1: recommended += products(role=data.role, limit=10-len(recommended), excluded=id)
    return product_list(data), recommended

def blogs(limit=0):
    data = list(reversed(article.objects.filter(active=True)))
    if limit: data = data[:limit]
    return [blog_list(ch) for ch in data]

def blog_details(id=0):
    data = article.objects.filter(id=id, active=True).first()
    if not data: return False
    data.views += 1
    data.save()
    return blog_list(data)

def default():
    data = {
        "status": True,
        "settings": settings(),
        "categories": categories(),
        "blogs": blogs(limit=10),
        "products": products(role=1, limit=10),
        "auctions": products(role=2, limit=10),
    }
    return data
