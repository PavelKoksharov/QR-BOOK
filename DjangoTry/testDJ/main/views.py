from datetime import *

from django.shortcuts import render, redirect

from .models import Books

from .templatetags.qr import *


def gen(request):
    data = request.POST.get("data")
    generateQR(data)
    books = Books.objects.filter(Free=True)
    return render(request, "qr/form.html", {"data": data,"books": books})


def delete(request):
    # city_pk_list = request.POST.get("Id")
    calendar1 = request.POST.get("calendar1")
    calendar2 = request.POST.get("calendar2")
    errors = ""
    books = Books.objects.filter(Free=True)
    if calendar1 is "" or calendar2 is "":
        errors = "Календарь должен быть заполнен"
        return render(request, "qr/form.html", {"errors": errors, "books": books})
    calendar1 = datetime.strptime(calendar1, "%Y-%m-%d")
    calendar2 = datetime.strptime(calendar2, "%Y-%m-%d")

    if datetime.now() > calendar2 or calendar2 < calendar1:
        errors = "Дата сдачи книги должна быть позже даты начала аренды книги"
        return render(request, "qr/form.html", {"errors": errors, "books": books})
    else:
        # p = Books.objects.get(Id=city_pk_list)
        p = Books.objects.get(Id=request.POST.get("book"))
        p.Free = False
        p.DateFirst = calendar1
        p.DateSecond = calendar2
        p.Reader = request.user.username
        p.save()
        return redirect("main")


def scan(request):
    scan = scanQR()
    books = Books.objects.filter(Free=True)

    if scan:
        return render(request, "qr/form.html", {"books": books, "scan": scan})
    return redirect("main")


def main(request):
    return render(request, "qr/main.html")


def catalog(request):
    books = Books.objects.all()
    return render(request, "qr/catalogue.html", {"books": books})


def instruction(request):
    return render(request, "qr/instruction.html")


def formBook(request):
    books = Books.objects.filter(Free=True)
    return render(request, "qr/form.html", {"books": books})


from django.shortcuts import get_object_or_404


def bookInfo(request, id):
    book = Books.objects.all().get(Id=id)

    # new = get_object_or_404(Books, Id=id)
    comment = Comments.objects.filter(new=id, moderation=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.new = book
            form.save()
    # else:
    form = CommentForm()
    return render(request, "qr/bookInfo.html", {"book": book,
                                                "comments": comment,
                                                "form": form})


# def bookInfo(request, id):
# book = Books.objects.all().get(Id=id)
# return render(request, "qr/bookInfo.html", {"book": book})


from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import logout, login


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'qr/register.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Регистрация"}
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'qr/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Авторизация"}
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')
