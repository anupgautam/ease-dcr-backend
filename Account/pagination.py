from rest_framework.pagination import PageNumberPagination
import json
from functools import wraps
from django.core.paginator import Paginator
from django.http import JsonResponse


class CustomPagination(PageNumberPagination):
    page_size = 200

def paginate_json_response(page_size=8):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if not isinstance(response, JsonResponse):
                raise TypeError("The view function must return a JsonResponse.")
            response_content = response.content.decode('utf-8')
            data = json.loads(response_content)
            queryset = data.get('results')
            paginator = Paginator(queryset, page_size)
            page_number = request.GET.get('page')
            paginated_queryset = paginator.get_page(page_number)

            paginated_data = {
                'links': {
                    'next': paginated_queryset.next_page_number() if paginated_queryset.has_next() else None,
                    'previous': paginated_queryset.previous_page_number() if paginated_queryset.has_previous() else None,
                },
                'count': paginator.count,
                'results': list(paginated_queryset),  # Convert queryset to list for JSON serialization
            }

            response.content = json.dumps(paginated_data).encode('utf-8')
            return response

        return wrapper

    return decorator