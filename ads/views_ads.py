import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import ADS, Category
from skypro_27 import settings
from users.models import User


@method_decorator(csrf_exempt, name='dispatch')
class AdsListView(ListView):
    model = ADS
    queryset = ADS.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # TODO возвращает все объявления в переданных ему категориях
        ad_cat = request.GET.getlist('cat', None)
        cat_q = None
        for cat in ad_cat:
            if not cat_q:
                cat_q = Q(category_id__exact=cat)
            else:
                cat_q |= Q(category_id__exact=cat)
        if cat_q:
            self.object_list = self.queryset.filter(cat_q)

        # TODO поиск по словам
        ad_text = request.GET.get('text', None)
        if ad_text:
            ad_text_q = Q(name__icontains=ad_text)
            ad_text_q |= Q(description__icontains=ad_text)
            self.object_list = self.queryset.filter(ad_text_q)

        # TODO поиск по локациям
        ad_location = request.GET.get('location', None)
        if ad_location:
            self.object_list = self.queryset.filter(author_id__locations__name__icontains=ad_location)

        # TODO диапазон цен, в котором мы готовы рассматривать товары
        ad_price_above = request.GET.get('price_from', None)
        ad_price_under = request.GET.get('price_to', None)
        if ad_price_above:
            self.queryset = self.queryset.filter(price__gte=ad_price_above)
        if ad_price_under:
            self.object_list = self.queryset.filter(price__lte=ad_price_under)

        # TODO pagination
        self.object_list = self.object_list.select_related('author').order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_ads = []
        for ads in page_obj:
            all_ads.append({
                "id": ads.id,
                "name": ads.name,
                "author_id": ads.author_id,
                "author": ads.author.first_name,
                "price": ads.price,
                "description": ads.description,
                "is_published": ads.is_published,
                "image": ads.image if ads.image else None,
                "category": ads.category.name,
                "category_id": ads.category_id,
            })

        response = {
            "items": all_ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = ADS
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)

        if ads_data['name'] is not None:
            self.object.name = ads_data['name']
        if ads_data['price'] is not None:
            self.object.price = ads_data['price']
        if ads_data['description'] is not None:
            self.object.description = ads_data['description']
        if ads_data['is_published'] is not None:
            self.object.is_published = ads_data['is_published']

        self.object.author = get_object_or_404(User, pk=ads_data['author'])
        self.object.category = get_object_or_404(Category, pk=ads_data['category'])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUploadImageView(UpdateView):
    model = ADS
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = ADS
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDetailView(DetailView):
    model = ADS

    def get(self, request, *args, **kwargs):
        try:
            ads = self.get_object()
        except:
            return JsonResponse({'error': "not found"}, status=404)

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author_id": ads.author_id,
            "author": ads.author.first_name,
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "image": ads.image if ads.image else None,
            "category_id": ads.category_id,
            "category": ads.category.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsPostView(CreateView):
    model = ADS
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ads_data['author'])
        category = get_object_or_404(Category, pk=ads_data['category'])

        ad = ADS()
        ad.name = ads_data["name"]
        ad.author = author
        ad.price = ads_data["price"]
        ad.description = ads_data["description"]
        ad.is_published = ads_data["is_published"]
        ad.category = category

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.first_name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image if ad.image else None,
            "category": ad.category.name,
            "category_id": ad.category_id,
        })
