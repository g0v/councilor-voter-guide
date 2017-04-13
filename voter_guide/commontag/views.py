from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(request, items, page_size=10):
    paginator = Paginator(items, page_size)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
