from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(request, items):
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
