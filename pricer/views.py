import operator
from collections import Counter
from django.http import JsonResponse # Django 1.7+
from django.core.cache import cache # low-level cache
from pricer.models import ItemSaleLH

# Original version, straight-forward approach. Turns out to be faster than using
# .values('list_price').annotate(num_items=Count('list_price')).order_by('-num_items')
def item_price(request):

    item = request.GET.get('item', '')
    city = request.GET.get('city', '')

    # see if we have answer in cache
    cache_key = 'ou_{}_{}'.format(item, city).replace (' ', '_')
    ret_val = cache.get(cache_key)
    if ret_val:
        # return cached value
        return ret_val

    if not item:
        ret_val = JsonResponse({'status': 404,
                                'content': { 'message': 'Not found' }})
        cache.set(cache_key, ret_val, 3600) # cache for 1 hour
        return ret_val

    list_prices = ItemSaleLH.objects.filter(title=item).values_list('list_price', flat=True).order_by() # no sort
    if city:
        list_prices = list_prices.filter(city=city)
    else:
        city = 'Not specified'

    # calculate the mode of list_prices
    total_count = 0
    price_counts = Counter()
    for list_price in list_prices:
        total_count += 1
        price_counts[list_price] += 1
    if not total_count:
        ret_val = JsonResponse({'status': 404,
                                'content': { 'message': 'Not found' }})
        cache.set(cache_key, ret_val, 3600) # cache for 1 hour
        return ret_val
    # suboptimal because we don't need to sort items less popular than the most popular one
    # find max, and all the values with same max value?
    sorted_price_counts = price_counts.most_common()
    # sorted_price_counts now contains the mode at the beginning. but there may be >1
    # sorted_price_counts = [(price, count), ...]
    price, count = sorted_price_counts[0]
    for price2, count2 in sorted_price_counts[1:]:
        if count2 != count:
            break
        if price2 > price:
            price = price2  # a popularity tie (same count), so keep the highest list price value

    content = {
        "item": item,
        "item_count": total_count, # example results are closer to count, but spec says total_count
        "price_suggestion": price,
        "city": city
    }
    ret_val = JsonResponse({'status': 200,
                            'content': content})
    cache.set(cache_key, ret_val, 3600) # cache for 1 hour
    return ret_val

