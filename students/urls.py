from django.urls import path
from .views import (
    profile_start, profile_step, profile_review,
    profile_submit, dashboard, upload_documents, profile_complete
)

urlpatterns = [
    path('start/', profile_start, name='profile_start'),
    path('step/<int:step>/', profile_step, name='profile_step'),
    path('review/', profile_review, name='profile_review'),
    path('submit/', profile_submit, name='profile_submit'),
    path('upload-documents/', upload_documents, name='upload_documents'),
    path('step/<int:step>/', profile_step, name='profile_step'),
    path('complete/', profile_complete, name='profile_complete'),
]
