from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from jobs.models import Job, Cities, JobTypes, Resume


# Create your views here.


def joblist(request):
    job_list = Job.objects.order_by('job_type')
    # template = loader.get_template("joblist.html")
    context = {'job_list': job_list}

    for job in job_list:
        job.city_name = next(b for a, b in Cities if a == job.job_city)
        job.job_type = JobTypes[job.job_type]
    # return HttpResponse(template.render(context, request))
    return render(request, 'joblist.html', context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        context = {'job': job}
        job.city_name = next(b for a, b in Cities if a == job.job_city)
    except Job.DoesNotExist:
        raise Http404('Job does not exist')
    return render(request, 'job.html', {'job': job})


class ResumeDetailView(DetailView):
    """   简历详情页    """
    model = Resume
    template_name = 'resume_detail.html'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """    简历职位页面  """
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone",
              "email", "apply_position", "gender",
              "bachelor_school", "master_school", "major", "degree",
              "candidate_introduction", "work_experience", "project_experience"]

    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())