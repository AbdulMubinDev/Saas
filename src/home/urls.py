from pathlib import path
from . import views

urlpatterns = [
    path('', views.home )
]
