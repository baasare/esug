from django.conf.urls.static import static
from django.urls import path

from esug import settings
from . import views

urlpatterns = [
    # Web
    path('', views.index, name='index'),
    path('vote', views.vote, name='vote'),
    path('results', views.results, name='results'),
    path('candidates', views.candidates, name='candidates'),
    path('candidate-detail/<int:candidate_id>', views.candidate_detail, name='candidate_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
