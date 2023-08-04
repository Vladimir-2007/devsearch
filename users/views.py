from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile, Message
from .form import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = None
        try:

            user = User.objects.get(username=username)

        except:
            messages.error(request, 'Пользователь с таким именем не существует')

        if user is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # ? --------------
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                messages.error(request, 'Имя пользователя или пароль введены не корректно')

    return render(request, 'users/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    messages.info(request, 'Пользователь покинул аккаунт')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Аккаунт пользователя был создан')

            login(request, user)

            return redirect('edit-account')
        else:
            messages.error(request, 'Во время регистрации произошла ошибка')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


# ? SEACH --------------
def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userprofile(request, pk):
    profile = Profile.objects.get(id=pk)

    topskills = profile.skills_set.exclude(description__exact='')
    otherskills = profile.skills_set.filter(description='')

    context = {'profile': profile, 'topSkills': topskills, 'otherSkills': otherskills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile  # ? <------------ проект принадлежит user
    skills = profile.skills_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)  # <---------? prefill information

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    page = 'create'
    profile = request.user.profile  # ? <------------ проект принадлежит user
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)  #
            skill.owner = profile
            skill.save()
            messages.success(request, "Навык был успешно создан")
            return redirect('account')

    context = {'form': form, 'page': page}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    page = 'update'
    profile = request.user.profile  # ? <------------ проект принадлежит user
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)  # ? <---------- prefill form

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)  # ? <---------- can modify
        if form.is_valid():
            form.save()
            messages.success(request, "Навык был успешно изменен")
            return redirect('account')

    context = {'form': form, 'page': page}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile  # ? <------------ проект принадлежит user
    skill = profile.skills_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Навык был успешно удален")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile  # ? <------------ проект принадлежит user
    messageRequests = profile.messages.all()  # ? <---------- related_name=messages in Model
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile  # ? <------------ проект принадлежит user
    message = profile.messages.get(id=pk)

    if message.is_read:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile  # ? <------------ проект принадлежит user
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Ваше сообщение было успешно отправлено!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
