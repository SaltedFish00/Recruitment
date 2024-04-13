from django.urls import re_path
from jobs import views

urlpatterns = [
    # 职位列表
    re_path(r"^joblist/", views.joblist, name="joblist"),
    # 职位详情
    re_path(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),
    # 提交简历
    re_path('resume/add/', views.ResumeCreateView.as_view(), name="resume-add"),
    # 提交详情
    re_path('resume/(?P<pk>\d+)/', views.ResumeDetailView.as_view(), name="resume-detail"),
    re_path(r"^$", views.joblist, name="name"),
]
