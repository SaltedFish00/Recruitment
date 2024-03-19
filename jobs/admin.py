from django.contrib import admin
from jobs.models import Job
# Register your models here.


class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date')

    def save_model(self, request, obj, form, change):
        obj.creator = request.user  # 创建人设置为当前登录的用户
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
