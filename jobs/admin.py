from datetime import datetime

from django.contrib import admin, messages

from interview.models import Candidate
from jobs.models import Job, Resume


# Register your models here.


class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date')

    def save_model(self, request, obj, form, change):
        obj.creator = request.user  # 创建人设置为当前登录的用户
        super().save_model(request, obj, form, change)


def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        resume_dict = resume.__dict__
        del resume_dict['id']
        # 把 obj 对象中的所有属性拷贝到 candidate 对象中:
        candidates = Candidate.objects.filter(phone=resume.phone)
        if candidates:
            messages.add_message(request, messages.INFO, '候选人: %s 已经在面试者名单中' % (candidate_names))
            return
        candidate.__dict__.update(resume_dict)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已成功进入面试流程' % (candidate_names))


enter_interview_process.short_description = u'进入面试流程'


class ResumeAdmin(admin.ModelAdmin):
    actions = (enter_interview_process,)

    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major',)

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience", "project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)
