from django.urls import path
from test_app.views import CategoryListCreateView, CategoryDetailUpdateDeleteView

urlpatterns = [
    path('', CategoryListCreateView.as_view()),
    path('<int:id>/', CategoryDetailUpdateDeleteView.as_view())
]
