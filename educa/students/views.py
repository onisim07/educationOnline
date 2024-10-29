from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course


class StudentRegistrationView(CreateView):
    '''Позволяет студентам регистрироваться на сайте'''
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    # Url-адрес перенаправления пользователя после успешной отправки формы:
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin,
                              FormView):
    '''Обслуживает зачисляемых на курсы студентов'''
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    '''Представления для просмотра курсов, на которые зачислены студенты'''
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получить объект Course:
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # Взять текущий модуль:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Взять первый модуль:
            context['module'] = course.modules.all()[0]
        return context
