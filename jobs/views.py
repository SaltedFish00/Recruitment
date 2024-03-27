from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader

from jobs.models import Job, Cities, JobTypes


# Create your views here.


def joblist(request):
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template("joblist.html")
    context = {'job_list': job_list}

    for job in job_list:
        job.city_name = next(b for a, b in Cities if a == job.job_city)
        job.job_type = JobTypes[job.job_type]

    return HttpResponse(template.render(context, request))


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        context = {'job': job}
        job.city_name = next(b for a, b in Cities if a == job.job_city)
    except Job.DoesNotExist:
        raise Http404('Job does not exist')
    return render(request, 'job.html', {'job': job})
