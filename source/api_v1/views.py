import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from api_v1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            article = get_object_or_404(Article, pk=kwargs.get('pk'))
            slr = ArticleSerializer(article)
            return JsonResponse(slr.data)


class ArticleUpdateView(View):
    def put(self, request, *args, **kwargs):
        article = get_object_or_404(Article.objects.all(), pk=kwargs.get('pk'))
        data = json.loads(request.body)
        srl = ArticleSerializer(instance=article, data=data, partial=True)
        if srl.is_valid(raise_exception=True):
            article = srl.update(article, srl.validated_data)
            return JsonResponse(srl.data, safe=False)
        else:
            response = JsonResponse(srl.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDeleteView(View):
    def delete(self, request, *args, **kwargs):
        article = get_object_or_404(Article.objects.all(), pk=kwargs.get('pk'))
        data = json.loads(request.body)
        srl = ArticleSerializer(instance=article, data=data, partial=True)
        if srl.is_valid(raise_exception=True):
            article = srl.delete(article)
            return JsonResponse(srl.data, safe=False)
        else:
            response = JsonResponse(srl.errors, safe=False)
            response.status_code = 400
            return response
