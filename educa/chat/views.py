from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@login_required
def course_chat_room(request, course_id):
    try:
        # Извлечь курс с заданным id,
        # к которому присоединился текущий пользователь:
        course = request.user.courses_joined.get(id=course_id)
    except:
        # Пользователь не является студентом курса либо курса нет:
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'course': course})



