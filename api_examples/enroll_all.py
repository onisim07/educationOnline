import requests


username = 'onisim'
password = '1234'
base_url = 'http://127.0.0.1:8000/api/'


# Извлечь все курсы:
r = requests.get(f'{base_url}courses/')
courses = r.json()

available_courses = ', '.join([course['title'] for course in courses])
print(f'Доступные курсы: {available_courses}')


for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f'{base_url}courses/{course_id}/enroll/',
                      auth=(username, password))
    if r.status_code == 200:
        # Успешный запрос
        print(f'Успешное зачисление на {course_title}')