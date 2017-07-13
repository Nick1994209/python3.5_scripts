import udacity


user = udacity.User('nick1994209@.ru', '')
name = user.name()

print(name)

# print out quiz completion rate in each course
for course in user.enrollments():
    print(course)
    prog = user.progress(course)
    print(prog)
    print('Course: ' + prog['title'])
    print('\t' + str(prog['quizzes_completed']) + '/'
            + str(prog['quiz_count']) + ' quizzes completed')