from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Project, Record
# Create your views here.
from .forms import RecordForm
from django.views.generic.edit import CreateView


class ProjectListView(generic.ListView, ):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context.update({
            'project_list': Project.objects.all(),
            'record_list': Record.objects.all(),
        })
        return context

    def post(self, request):
        project = [i.name for i in Project.objects.all()]
        record = [i.text for i in Record.objects.all()]
        str_addrecord = []
        str_deleterecord = []
        str_record_add = []
        str_checkbox = []
        str_deleteproject=[]
        for p in project:
            add_str = 'record_field_' + str(p)
            del_str = 'deleteproject_'+str(p)
            str_record_add.append(add_str)
            str_deleteproject.append(del_str)

        for p in project:
            add_str = 'addrecord_' + str(p) + '_'
            checkbox_str = 'checkbox_'+ str(p) + '_'
            delete_str = 'deleterecord_' + str(p) + '_'
            for r in record:
                add_str += str(r)
                checkbox_str += str(r)
                delete_str += str(r)
                str_deleterecord.append(delete_str)
                str_addrecord.append(add_str)
                str_checkbox.append(checkbox_str)
                checkbox_str = 'checkbox_' + str(p) + '_'
                add_str = 'addrecord_' + str(p) + '_'
                delete_str = 'deleterecord_' + str(p) + '_'
        str_list = str_addrecord + str_deleterecord
        if request.method == "POST":
            for item in str_list:
                if item in request.POST:
                    if "addrecord" in item:
                        print("add")
                    else:
                        print("del")
                        for project in Project.objects.all():
                            if item.split('_')[1] == project.name:
                                print(project.name)
                                for r in Record.objects.all():
                                    if item.split('_')[2] == r.text:

                                        Record.objects.filter(project__name=project, text = r.text).delete()
                                        break
                                break

            for item in str_record_add:
                if item in request.POST:
                    data = dict(request.POST)

                    check = True

                    for project in Project.objects.all():
                        if str(list(data.keys())[1]).split('_')[2] == project.name:
                            for record in Record.objects.filter(project=project):
                                if list(data.values())[1][0] == record.text:
                                    check = False
                            if check:
                                if list(data.values())[1][0] != '':
                                    Record.objects.create(text=list(data.values())[1][0], project=project)
                            break

            for item in str_checkbox:
                print(request.POST)
                if item in request.POST:
                    print(item)
                    for project in Project.objects.all():
                        if item.split('_')[1] == project.name:
                            print(project.name)
                            print(request.POST[item])
                            for r in Record.objects.all():
                                if item.split('_')[2] == r.text:
                                    if r.status == 0:
                                        print("1")
                                        Record.objects.filter(project__name=project, text=r.text).update(status = 1)
                                        break
            if 'add_list' in request.POST:
                data = dict(request.POST)
                if list(data.values())[1][0] != '':
                    Project.objects.create(name=list(data.values())[1][0])

            for item in str_deleteproject:

                if item in request.POST:
                    print(item)
                    for project in Project.objects.all():
                        if item.split('_')[1] == project.name:
                            Record.objects.filter(project=project).delete()
                            Project.objects.filter(name=project.name).delete()

                            break
        context = {
            'project_list': Project.objects.all(),
            'record_list': Record.objects.all()}
        return render(request, "catalog/project_list.html", context)
