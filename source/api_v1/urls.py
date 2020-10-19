from django.urls import path, include

from api_v1.views import *

app_name = 'api_v1'

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),

    path('article/', include([
        path('create/', ArticleCreateView.as_view(), name='article_create'),
        path('<int:pk>/', include([
            path('', ArticleDetailView.as_view(), name='article_view'),
            path('update/', ArticleUpdateView.as_view(), name='article_update'),
            path('delete/', ArticleDeleteView.as_view(), name='article_delete'),
        ])),
    ])),
]
