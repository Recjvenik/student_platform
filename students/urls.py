from django.urls import path
from .views import (
    profile_start, profile_step, save_step, profile_review,
    profile_submit, dashboard, upload_documents
)

urlpatterns = [
    path('start/', profile_start, name='profile_start'),
    path('step/<int:step>/', profile_step, name='profile_step'),
    path('save-step/', save_step, name='save_step'),
    path('review/', profile_review, name='profile_review'),
    path('submit/', profile_submit, name='profile_submit'),
    path('upload-documents/', upload_documents, name='upload_documents'),
]

# Dashboard URL at root level
from django.urls import path
from .views import dashboard

urlpatterns += [
    path('../dashboard/', dashboard, name='dashboard'),
]