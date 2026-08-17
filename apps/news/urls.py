from django.urls import path
from . import views

app_name = 'news'          # ← это обязательно!

urlpatterns = [                   # /news/
    path('<slug:slug>/', views.detail, name='detail'),    # /news/kakaya-to-novost/
]