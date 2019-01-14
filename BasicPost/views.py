# coding=utf-8
from django.utils import timezone
from BasicPost.models import Gallary,Images, ProjectBoard, SeminarBoard, NoticeBoard,NewsBoard
from administrator.models import User,MainImage
from django.shortcuts import render, get_object_or_404
from .forms import GallaryForm, ProjectBoardForm,SeminarBoardForm, NoticeBoardForm,NewsBoardForm
from django.shortcuts import redirect
## 페이지네이션 구현
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
## 이미지 여러개 위한것
from django.forms import modelformset_factory
from django.db.models import Q
from .security import security_views
from administrator.security import security_views as admin_sec

def del_file(old_file, new_file):
    if old_file != new_file:
        old_file.delete()
    return new_file

def del_image(old_image, new_image):
    if old_image.name != new_image.name:
        old_image.delete()
    return new_image

def auth_test(request):
    check=security_views.auth_test(request)
    return check

# Create your views here.
def index(request):
    check=auth_test(request)
    news = NewsBoard.objects.all().order_by('-origin_date')
    projects = ProjectBoard.objects.all().order_by('-origin_date')
    seminars = SeminarBoard.objects.all().order_by('-origin_date')
    main = security_views.main(request)
    return render(request, 'blog/index.html', {'main':main, 'news': news, 'projects': projects, 'seminars':seminars,'check':check})

def album(request):
    check = auth_test(request)
    gallaries = Gallary.objects.all().order_by('-origin_date')
    paginator = Paginator(gallaries, 6)
    page = request.GET.get('page')

    try:
        gallaries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gallaries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gallaries = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'blog/album.html', {
        'gallaries': gallaries,
        'max_index' : max_index,
        'check': check,
    })

def album_new(request):
    check = auth_test(request)
    if admin_sec.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=5, max_num=5)
    if request.method == "GET":
        form = GallaryForm()
        formset = ImageFormset(queryset=Images.objects.none())
    elif request.method == "POST":
        form = GallaryForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            gallary = form.save(commit=False)
            gallary.origin_date = timezone.now()
            gallary.final_date=timezone.now()
            gallary.writer_name = check['name']
            gallary.writer_id = check['id']
            gallary.save()

            for f in formset:
                try:
                    photo=Images(post=gallary, image=f.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('album')
    return render(request, 'blog/album_edit.html',
                  {'form': form, 'formset': formset,'check': check})


def album_detail(request, pk):
    check = auth_test(request)
    gallary = get_object_or_404(Gallary, pk=pk)
    return render(request, 'blog/album_detail.html', {'gallary': gallary, 'check':check})

def edit_check(request, check, post):
    if check==False:
        return 1
        return render(request, 'blog/reject.html')
    elif check['id']!=post.writer_id:
        return 2
        return render(request, 'blog/auth_restrict.html')

def album_edit(request, pk):
    check = auth_test(request)
    gallary = get_object_or_404(Gallary, pk=pk)
    if edit_check(request, check, gallary)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, gallary)==2:
        return render(request, 'blog/auth_restrict.html')
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=5, max_num=5)
    if request.method == "POST":
        form = GallaryForm(request.POST or None, instance=gallary)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            gallary = form.save(commit=False)
            gallary.final_date = timezone.now()
            gallary.writer_name=check['name']
            gallary.save()
            # image check - 프롬프트 창 확인
            #print(formset.cleaned_data)
            data=Images.objects.filter(post=gallary)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Images(post=gallary, image=f.cleaned_data['image'])
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = Images(post=gallary, image=f.cleaned_data['image'])
                        d=Images.objects.get(id=data[index].id)
                        d.image=photo.image
                        d.save()


            return redirect(album)
    else:
        form = GallaryForm(instance=gallary)
        formset = ImageFormset(queryset=Images.objects.filter(post=gallary))
    return render(request, 'blog/album_edit.html', {'gallary': gallary, 'form': form, 'formset': formset, 'check':check})

def album_remove(request, pk):
    check = auth_test(request)
    post = get_object_or_404(Gallary, pk=pk)
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    post.delete()
    return redirect('album')

def members(request):
    check = auth_test(request)
    members = User.objects.filter(~Q(name="admin")).order_by('name')

    return render(request, 'blog/members.html', {'members': members, 'check':check})

def members_radix(request, radix):
    check = auth_test(request)
    # In Python 3, str is a Unicode string.
    str_radix=str(", "+str(radix)+"기")
    members_radix = User.objects.filter(class_field__contains=str_radix).order_by('name')
    #print(members_radix[0].class_field)

    return render(request, 'blog/members_radix.html', {'members_radix': members_radix, 'radix': members_radix[0].class_field, 'check':check})


def news(request):
    check = auth_test(request)
    posts = NewsBoard.objects.all().order_by('-origin_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'blog/news.html', {
        'posts': posts,
        'max_index': max_index,
        'check': check
    })



def news_new(request):
    check = auth_test(request)
    if admin_sec.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if request.method == "GET":
        form = NewsBoardForm()
    elif request.method == "POST":
        form = NewsBoardForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.origin_date = timezone.now()
            post.final_date = timezone.now()
            post.writer_name=check['name']
            post.writer_id=check['id']
            post.save()
            return redirect(news)
    ctx = {
        'form': form,
        'check': check
    }

    return render(request, 'blog/news_edit.html', ctx)

def news_edit(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NewsBoard, pk=pk)
    old_image = post.image
    old_file=post.file
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    if request.method == "POST":
        form = NewsBoardForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.final_date = timezone.now()
            new_image=post.image
            new_file=post.file
            post.image=del_image(old_image, new_image)
            post.file=del_file(old_file, new_file)
            post.save()
            return redirect('news_detail', pk=post.pk)
    else:
        form = NewsBoardForm(instance=post)
    return render(request, 'blog/news_edit.html', {'post': post,'form': form, 'check':check})

def news_detail(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NewsBoard, pk=pk)
    return render(request, 'blog/news_detail.html', {'post': post, 'check':check})

def news_remove(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NewsBoard, pk=pk)
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    post.delete()
    return redirect('news')


def seminar(request):
    check = auth_test(request)
    posts = SeminarBoard.objects.all().order_by('-origin_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'blog/seminar.html', {
        'posts': posts,
        'max_index': max_index,
        'check': check
    })



def seminar_new(request):
    check = auth_test(request)
    if admin_sec.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if request.method == "GET":
        form = SeminarBoardForm()
    elif request.method == "POST":
        form = SeminarBoardForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.origin_date = timezone.now()
            post.final_date = timezone.now()
            post.writer_name = check['name']
            post.writer_id = int(check['id'])
            post.save()
            return redirect(seminar)
    ctx = {
        'form': form,
        'check': check
    }

    return render(request, 'blog/seminar_edit.html', ctx)


def seminar_detail(request, pk):
    check = auth_test(request)
    post = get_object_or_404(SeminarBoard, pk=pk)
    return render(request, 'blog/seminar_detail.html', {'post': post, 'check':check})



def seminar_edit(request, pk):
    check = auth_test(request)
    post = get_object_or_404(SeminarBoard, pk=pk)
    old_image = post.image
    old_file = post.file
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')

    if request.method == "POST":
        form = SeminarBoardForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.final_date = timezone.now()
            new_image=post.image
            new_file=post.file
            post.image=del_image(old_image, new_image)
            post.file=del_file(old_file, new_file)
            post.save()
            return redirect('seminar_detail', pk=post.pk)
    else:
        form = SeminarBoardForm(instance=post)
    return render(request, 'blog/seminar_edit.html', {'post': post,'form': form, 'check':check})

def seminar_remove(request, pk):
    check = auth_test(request)
    post = get_object_or_404(SeminarBoard, pk=pk)
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    post.delete()
    return redirect('seminar')


def project(request):
    check = auth_test(request)
    posts = ProjectBoard.objects.all().order_by('-origin_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'blog/project.html', {
        'posts': posts,
        'max_index': max_index,
        'check': check
    })



def project_new(request):
    check = auth_test(request)
    if admin_sec.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if request.method == "GET":
        form = ProjectBoardForm()
    elif request.method == "POST":
        form = ProjectBoardForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.origin_date = timezone.now()
            post.final_date = timezone.now()
            post.writer_name = check['name']
            post.writer_id = check['id']
            post.save()
            return redirect(project)
    ctx = {
        'form': form,
        'check': check
    }

    return render(request, 'blog/project_edit.html', ctx)


def project_detail(request, pk):
    check = auth_test(request)
    post = get_object_or_404(ProjectBoard, pk=pk)
    return render(request, 'blog/project_detail.html', {'post': post, 'check':check})



def project_edit(request, pk):
    check = auth_test(request)
    post = get_object_or_404(ProjectBoard, pk=pk)
    old_image = post.image
    old_file = post.file
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    if request.method == "POST":
        form = ProjectBoardForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.final_date = timezone.now()
            new_image=post.image
            new_file=post.file
            post.image=del_image(old_image, new_image)
            post.file=del_file(old_file, new_file)
            post.save()
            return redirect('project_detail', pk=post.pk)
    else:
        form = ProjectBoardForm(instance=post)
    return render(request, 'blog/project_edit.html', {'post': post,'form': form, 'check':check})

def project_remove(request, pk):
    check = auth_test(request)
    post = get_object_or_404(ProjectBoard, pk=pk)
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    post.delete()
    return redirect('project')


def recruit(request):
    check = auth_test(request)
    return render(request, 'blog/recruit.html',{'check':check})


def about(request):
    check = auth_test(request)
    return render(request, 'blog/about.html',{'check':check})


def rules(request):
    check = auth_test(request)
    return render(request, 'blog/rules.html',{'check':check})


def notice(request):
    check = auth_test(request)
    posts = NoticeBoard.objects.all().order_by('-origin_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    return render(request, 'blog/notice.html', {
        'posts': posts,
        'max_index': max_index,
        'check': check
    })



def notice_new(request):
    check = auth_test(request)
    if admin_sec.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if request.method == "GET":
        form = NoticeBoardForm()
    elif request.method == "POST":
        form = NoticeBoardForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.origin_date = timezone.now()
            post.final_date = timezone.now()
            post.writer_name=check['name']
            post.writer_id=check['id']
            post.save()
            return redirect(notice)
    ctx = {
        'form': form,
        'check': check
    }

    return render(request, 'blog/notice_edit.html', ctx)

def notice_edit(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NoticeBoard, pk=pk)
    old_image = post.image
    old_file=post.file
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    if request.method == "POST":
        form = NoticeBoardForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.final_date = timezone.now()
            new_image=post.image
            new_file=post.file
            post.image=del_image(old_image, new_image)
            post.file=del_file(old_file, new_file)
            post.save()
            return redirect('notice_detail', pk=post.pk)
    else:
        form = NoticeBoardForm(instance=post)
    return render(request, 'blog/notice_edit.html', {'post': post,'form': form, 'check':check})

def notice_detail(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NoticeBoard, pk=pk)
    return render(request, 'blog/notice_detail.html', {'post': post, 'check':check})

def notice_remove(request, pk):
    check = auth_test(request)
    post = get_object_or_404(NoticeBoard, pk=pk)
    if edit_check(request, check, post)==1:
        return render(request, 'blog/reject.html')
    elif edit_check(request, check, post)==2:
        return render(request, 'blog/auth_restrict.html')
    post.delete()
    return redirect('notice')