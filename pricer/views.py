import operator

from django.shortcuts import render
from django.http import JsonResponse # Django 1.7+

from pricer.models import ItemSale, ItemSaleLH

def item_price(request):
    def ret_404():
        # could just create str_404, but doing so uses CPU for non-404 cases
        return JsonResponse({
            'status': 404,
            'content': { 'message': 'Not found' }})

    item = request.GET.get('item', '')
    city = request.GET.get('city', '')
    if not item:
        return ret_404()
    list_prices = ItemSaleLH.objects.filter(title=item).values_list('list_price', flat=True).order_by() # no sort
    if city:
        list_prices = list_prices.filter(city=city)
    else:
        city = 'Not specified'
    total_count = list_prices.count()
    if not total_count:
        return ret_404()
    # calculate the mode of list_prices
    price_counts = {}
    #print 'BEGIN list_prices ------'
    for list_price in list_prices:
        # print list_price,
        if list_price in price_counts:
            price_counts[list_price] += 1
        else:
            price_counts[list_price] = 1
    #print 'END------BEGIN sorted_list_prices'
    sorted_list_prices = sorted(list_prices)
    #print sorted_list_prices
    #print '----- END -----'
    # suboptimal because we don't need to sort items less popular than the most popular one
    # find max, and all the values with same max value?
    sorted_price_counts = sorted(price_counts.items(), key=operator.itemgetter(1), reverse=True)
    # sorted_price_counts now contains the mode at the beginning. but there may be >1
    # sorted_price_counts = [(price, count), ...]
    price, count = sorted_price_counts[0]
    for i in range(1, len(sorted_price_counts)):
        if count != sorted_price_counts[i][1]:
            break
        if sorted_price_counts[i][0] > price:
            # a popularity tie (same count), so keep the highest list price value
            price = sorted_price_counts[i][0]

    content = {
        "item": item,
        "item_count": total_count, # example results are closer to count, but spec says total_count
        "price_suggestion": price,
        "city": city
    }
    return JsonResponse({'status': 200,
                         'content': content})

