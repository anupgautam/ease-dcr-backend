from Product.models import CompanyProduct
from django.db.models import Count
from Product.models import Product
from django.apps import apps
from django.http import JsonResponse
from dailycallrecord.models import *
from django.db.models import Max
import json

def get_product_graph():
    max_count = CompanyProduct.objects.filter(company_name=1, created_date="2022-12-23 14:53:49.456765+05:45").values('product_name').annotate(
    count=Count('product_name')).order_by('-count')
    max_value =  max_count.first()
    
    top_10_value = max_count[:10]
    values = []
    count = []
    for i in top_10_value:
        instance = Product.objects.get(id=i['product_name'])
        values.append(instance.product_name)
        count.append(i['count'])
    
    
    
    


# this method returns the maximum product ordered by
# the chemist and stockist
def get_maximum_ordered_product(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    max_quantity = DcrForStockist.objects.all().aggregate(Max('ordered_quantity'))['ordered_quantity__max']
    final_dict = DcrForStockist.objects.filter(ordered_quantity=max_quantity,created_date__range=(start_date, end_date)).order_by('pk').values('visited_stockist__stockist_name__stockist_name','ordered_product__product_name__product_name','ordered_quantity')[:5]
    dict = list(final_dict.values('visited_stockist__stockist_name__stockist_name','ordered_product__product_name__product_name','ordered_quantity')[:5])

    max_quantity = DcrForChemist.objects.all().aggregate(Max('ordered_quantity'))['ordered_quantity__max']
    final_dict1 = DcrForChemist.objects.filter(ordered_quantity=max_quantity,created_date__range=(start_date, end_date)).order_by('pk').values('visited_chemist__chemist_name','ordered_product__product_name','ordered_quantity')[:5]
    dict2 = list(final_dict1.values('visited_chemist__chemist_name','ordered_product__product_name','ordered_quantity')[:5])

    final_dict = {
        'stockist':dict,
        'chemist':dict2
    }
    return final_dict


class Graph:
    
    class Meta:
        abstract = True

    def get_graph(self):
        pass

class OptimizedGraph(Graph):
    def __init__(self, model_name: str, app_name:str, company_name:str, created_date:str, filter_field:str, counting_field:str, values_counter:int, displaying_field:str, parent_model:str) -> None:
        self.model_name = model_name
        self.company_name = company_name
        self.app_name = app_name
        self.created_date = created_date
        self.filter_field = filter_field
        self.counting_field = counting_field
        self.values_counter = values_counter
        self.displaying_field = displaying_field
        self.parent_model = parent_model
    def get_graph(self):
        model = apps.get_model(self.app_name, self.model_name)
        max_count = model.objects.filter(company_name=self.company_name, created_date=self.created_date).values(self.filter_field).annotate(
            count=Count(self.counting_field)).order_by('-count')
        max_value = max_count.first()
        top_10_value = max_count[:self.values_counter]
        values = []
        count = []
        
        for i in top_10_value:
            instance = apps.get_model(self.app_name, self.parent_model).objects.get(id=i[self.filter_field])
            values.append(getattr(instance, self.filter_field))
            count.append(i['count'])
        graph_data = {
            'values': values,
            'count': count
        }
        return graph_data
        