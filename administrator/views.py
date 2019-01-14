# coding=utf-8
from django.shortcuts import get_object_or_404, render
from .models import User, MainImage
from registration.models import UserRequest
from .forms import UserInfoForm, MainImageForm
from django.shortcuts import redirect
from BasicPost.views import auth_test, del_image
from django.db.models import Q
from .security import security_views

def administrator(request):
    check = auth_test(request)
    if security_views.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if security_views.authorization(request, check):
        return render(request, 'administrator/admin_reject.html', {'check': check})
    #latest_question_list0 = Question.objects.all()[0]
    #latest_question_list1 = Question.objects.all()[1]
    latest_UserRequest_list = UserRequest.objects.all().order_by('name')
    latest_User_list = User.objects.filter(~Q(name="admin")).order_by('name')

    context = {
        #'latest_question_list0': latest_question_list0,
        #'latest_question_list1': latest_question_list1,
        'latest_UserRequest_list': latest_UserRequest_list,
        'latest_User_list': latest_User_list,
        'check': check,
    }

    return render(request, 'administrator/admin_main.html', context)


def okay(request, userRequest_student_id):
    check = auth_test(request)
    if security_views.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if security_views.authorization(request, check):
        return render(request, 'administrator/admin_reject.html', {'check': check})
    if request.method == 'POST' and 'btn1' in request.POST:
        userRequest = UserRequest.objects.get(student_id=userRequest_student_id)
        user = User()
        user.name = userRequest.name
        user.e_mail = userRequest.e_mail
        user.password = userRequest.password
        user.github = userRequest.github
        user.major = userRequest.major
        user.sns_address = userRequest.sns_address
        user.student_id = userRequest.student_id
        user.phone = userRequest.phone
        user.introduction = userRequest.introduction
        # user.image = userRequest.image
        user.save()

        userRequest.delete()
        return redirect('administrator')

    elif request.method == 'POST' and 'btn2' in request.POST:
        deny = UserRequest.objects.get(student_id=userRequest_student_id)
        deny.delete()

        return redirect('administrator')


def detail(request, user_student_id):
    check = auth_test(request)
    if security_views.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if security_views.authorization(request, check):
        return render(request, 'administrator/admin_reject.html', {'check': check})
    user = get_object_or_404(User, student_id=user_student_id)
    if user.name == 'admin':
        return render(request, 'administrator/admin_reject.html', {'check': check})
    form = UserInfoForm(instance=user)
    context = {
        'user': user,
        'form': form,
        'check': check
    }

    return render(request, 'administrator/detail.html', context)


def modify(request, user_student_id):
    check = auth_test(request)
    if security_views.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if security_views.authorization(request, check):
        return render(request, 'administrator/admin_reject.html', {'check': check})
    user = get_object_or_404(User, student_id=user_student_id)
    old_image = user.image

    if request.method == 'POST' and 'btn1' in request.POST:
        form = UserInfoForm(request.POST, request.FILES, instance=user)
        post = form.save(commit=False)
        new_image = post.image
        post.image = del_image(old_image, new_image)
        post.save()
        return redirect('administrator')

    elif request.method == 'POST' and 'btn2' in request.POST:
        user.delete()
        return redirect('administrator')


'''        
def mainImage_detail(request):
'''


def mainImage_edit(request):
    check = auth_test(request)
    post = get_object_or_404(MainImage, id=1)
    old_image1 = post.image1
    old_image2 = post.image2
    if security_views.are_you_login(request, check):
        return render(request, 'blog/reject.html', {'check': check})
    if security_views.authorization(request, check):
        return render(request, 'administrator/admin_reject.html', {'check': check})
    try:
        # post = MainImage.objects.all()
        if request.method == "POST":
            form = MainImageForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                new_image1 = post.image1
                post.image1 = del_image(old_image1, new_image1)
                new_image2 = post.image2
                post.image2 = del_image(old_image2, new_image2)
                post.save()
                return redirect('administrator')
        else:
            form = MainImageForm(instance=post)
        return render(request, 'administrator/mainImage_edit.html', {'check': check, 'form': form})
    except:
        if request.method == "POST":
            form = MainImageForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('administrator')
        else:
            form = MainImageForm()
        return render(request, 'administrator/mainImage_edit.html', {'check': check, 'form': form})