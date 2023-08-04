from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 3)

    context = {
        'projects': projects,
        'search_query': search_query,
        'paginator': projects,
        'custom_range': custom_range
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = project.tags.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile  # ? <------------ проект принадлежит user
        review.save()

        project.getVoteCount

        messages.success(request, 'Ваш отзыв был успешно добавлен')
        return redirect('project', pk=project.id)

    return render(request, 'projects/single-project.html', {'project': project, 'tags': tags, 'form': form})


@login_required(login_url='login')
def createproject(request):
    page = 'create'
    profile = request.user.profile  # ? <------------ проект принадлежит user
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form, 'page': page}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateproject(request, pk):
    page = 'update'
    profile = request.user.profile  # ? <------------ проект принадлежит user
    # project = Project.objects.get(id=pk)
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form, 'page': page, 'project': project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteproject(request, pk):
    profile = request.user.profile  # ? <------------ проект принадлежит user
    # project = Project.objects.get(id=pk)
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
