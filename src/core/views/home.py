from src.core.config.main import *

def categories():
    products_count = product.objects.all().count()
    all_categories = category.objects.filter(active=True)
    categories = []
    others, index = 0, 0
    for ch in all_categories:
        if index > 2: break
        count = product.objects.filter(category_id=ch.id).count()
        if count:
            categories.append([ch.name.split(' ')[0], count])
            index += 1
            others += count
    others = products_count - others
    if others: categories.append(['others', others])
    return categories

def profit():
    income, expenses = 0, 0
    sales = order.objects.all()
    for ch in sales: income += ch.price
    _profit_ = big_number(int(income - expenses))
    income = big_number(int(income))
    expenses = big_number(int(expenses))
    return income, expenses, _profit_

@authentication
def index(request):
    data = start_data(request)
    data['orders_count'] = big_number(order.objects.all().count())
    data['income'], data['expenses'], data['profit'] = profit()
    data['categories'] = categories()
    return render(request, 'index.html', data)
