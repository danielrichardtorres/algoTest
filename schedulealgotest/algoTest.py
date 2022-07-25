from api.models import Student, Teacher, Subject, appInstance, reoccuringApp, TimeSlot
from rest_framework import viewsets
from faker import Faker
import random
import datetime

list_of_school_subjects = [
    "SAT Math",
    "SAT Reading",
    "SAT Writing",
    "ACT Math",
    "ACT Reading",
    "ACT Writing",
    "AP Calculus AB",
    "AP Calculus BC",
    "AP Statistics",
    "AP Physics C",
]
day_choices = TimeSlot.day_choices
day_indexes = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
}


fake = Faker()
start_time_choices = TimeSlot.start_time_choices
end_time_choices = TimeSlot.end_time_choices


def clearAll():
    # delete all existing data
    obj, created = Student.objects.all().delete()
    obj, created = Teacher.objects.all().delete()
    obj, created = Subject.objects.all().delete()
    obj, created = appInstance.objects.all().delete()
    obj, created = reoccuringApp.objects.all().delete()
    obj, created = TimeSlot.objects.all().delete()


def fillSubjects():
    # use list of school subjects to create subjects
    for subject in list_of_school_subjects:
        x = Subject.objects.create(name=subject)


def makeStudents(num=10):
    # use faker to generate fake students
    for i in range(num):
        fake = Faker()
        x = Student.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
        )


def makeTeachers(numTeach=10, numSubjs=4):
    for i in range(numTeach):
        fake = Faker()
        x = Teacher.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
        )
    # for each teacher assign them a random number of subjects
    for teacher in Teacher.objects.all():
        for i in range(numSubjs):
            x = teacher.subjects.add(random.choice(Subject.objects.all()))
        teacher.save()
    covered_subjects = set()
    for teacher in Teacher.objects.all():
        for subject in teacher.subjects.all():
            covered_subjects.add(subject.name)
    # make sure at least one teacher teachers the not covered subjects
    for subject in list_of_school_subjects:
        if subject not in covered_subjects:
            teacher = random.choice(Teacher.objects.all())
            x = teacher.subjects.add(Subject.objects.get(name=subject))
            x = teacher.save()


def make_time_slots():
    # create all the time slots for the week (monday - friday)
    for i in range(5):
        for j in range(3):
            x = TimeSlot.objects.create(
                day=day_choices[i][0],
                start_time=start_time_choices[j][0],
                end_time=end_time_choices[j][0],
            )


def makeWeeklyApps(num_apps_per_student=2):
    # create a reoccuring weekly app for each student
    for student in Student.objects.all():
        for i in range(num_apps_per_student):
            x = reoccuringApp.objects.create(
                student=student,
                subject=random.choice(Subject.objects.all()),
            )
            random_time_slot = list(TimeSlot.objects.all())[
                random.randint(0, len(list(TimeSlot.objects.all())) - 1)
            ]
            x.time_slot.add(random_time_slot)
            x.save()


def makeTeacherAvailability():
    # randomly assign 1 of the time slots to each teachers availability
    for teacher in Teacher.objects.all():
        for i in range(2):
            x = teacher.availability.add(random.choice(TimeSlot.objects.all()))
        teacher.save()


def make_appointments():
    # match the teachers with available time slots to create app instances for next week
    # make sure of the following
    # 1. the reoccuringApp subject is one of the teachers subjects
    # 2. the reoccuringApp day is one of the teachers availability days
    # 3. the reoccuringApp time is one of the teachers availability times on the same day
    # 4. only one appointment for the student subject date and time is made
    todays_date = datetime.date.today()
    today_int = datetime.date.today().weekday() + 1
    for app in reoccuringApp.objects.all():
        for teacher in Teacher.objects.all():
            if app.subject in teacher.subjects.all():
                for day in [d[0] for d in day_choices]:
                    if day in teacher.availability.values_list("day", flat=True):
                        for time in teacher.availability.values_list(
                            "start_time", flat=True
                        ):
                            app_time = app.time_slot.first().start_time
                            if time == app_time:
                                # get the app day as a int from days_of_week
                                app_day = app.time_slot.first().day
                                app_int = day_indexes[app_day]
                                diff = app_int - today_int
                                newday = todays_date + datetime.timedelta(days=diff + 7)
                                # print(app_int, today_int, diff, newday)
                                # make sure only one appointment is made for the student subject date and time
                                if (
                                    appInstance.objects.filter(
                                        student=app.student,
                                        subject=app.subject,
                                        date=newday,
                                        time=app_time,
                                    ).count()
                                    == 0
                                    and appInstance.objects.filter(
                                        teacher=teacher,
                                        subject=app.subject,
                                        date=newday,
                                        time=app_time,
                                    ).count()
                                    == 0
                                ):
                                    appInstance.objects.create(
                                        student=app.student,
                                        teacher=teacher,
                                        subject=app.subject,
                                        date=newday,
                                        time=time,
                                    )


def getError():
    # get the number of reoccuring apps
    num_reoccuring_apps = reoccuringApp.objects.all().count()
    # get the number of app instances
    num_app_instances = appInstance.objects.all().count()
    # print the difference
    return num_reoccuring_apps - num_app_instances


# original code
# clearAll()
# fillSubjects()
# makeStudents()
# makeTeachers()
# make_time_slots()
# makeWeeklyApps(2)
# makeTeacherAvailability()
# make_appointments()
# print(getError())
# end of original code

# find all schedules code
# def getTeacherAvailabilities():
#     # a list of teacher avalability to subjects to timeslots
#     teacher_availability = {}
#     for teacher in Teacher.objects.all():
#         teacher_availability[teacher.id] = {}
#         subjects = teacher.subjects.all()[::1]
#         for time_slot in teacher.availability.all():
#             teacher_availability[teacher.id][time_slot.id] = subjects
#     print()
#     print("teacher_availability:")
#     print(teacher_availability)
#     return teacher_availability


# def countTimeSlots():
#     # count the number of teachers in each time slot
#     time_slot_count = {}
#     for time_slot in TimeSlot.objects.all():
#         time_slot_count[time_slot.id] = 0
#     for teacher in Teacher.objects.all():
#         for time_slot in teacher.availability.all():
#             time_slot_count[time_slot.id] += 1
#     print()
#     print("Time Slots:")
#     [print(str(ts), time_slot_count[ts]) for ts in time_slot_count]
#     return time_slot_count


def getReoccuringApps():
    # a list of reoccuring apps to subjects to timeslots
    reoccuring_apps = {}
    for app in reoccuringApp.objects.all():
        reoccuring_apps[app.id] = [
            app.time_slot.first().id,
            app.student.id,
            app.subject.id,
        ]
    print()
    print("Reoccuring Apps:")
    print(reoccuring_apps)
    return reoccuring_apps


# getTeacherAvailabilities()
# getReoccuringApps()

# generate a dictionary with the subjects and their teachers and timeslots
def getSubjects():
    subjects = {}
    for teacher in Teacher.objects.all():
        for subject in teacher.subjects.all():
            if subject not in subjects:
                subjects[subject.id] = []
            subjects[subject.id] = [
                teacher.id,
                [x.id for x in teacher.availability.all()],
            ]
    print()
    print("Subjects:")
    print(subjects)
    return subjects


subject_availability = getSubjects()
reoccuringApps = getReoccuringApps()

# print(reoccuringApps)

# recursively find all schedules by removing teacher from availability and adding to schedule list of schedules
all_schedules = []
mySchedule = list()

# good_schedule = "fail"
# import copy


# def findGoodSchedule(reoccuringApps, subject_availability, mySchedule):
#     for app_id, values in reoccuringApps.items():
#         for time_slot_id, app_subject_id, app_student in values:
#             # actual_re = reoccuringApp.objects.get(id=app_id)
#             # actual_ts = TimeSlot.objects.get(id=time_slot_id)
#             # actual_sj = Subject.objects.get(id=subject_id)
#             if app_subject_id in subject_availability.keys():
#                 for teacher_id, time_slots in subject_availability[app_subject_id]:
#                     if time_slot_id in time_slots:
#                         # add teacher/subject/time_slot/student to mySchedule
#                         mySchedule.append((teacher_id, app_subject_id, time_slot_id))


# good_schedule = findGoodSchedule(reoccuringApps, subject_availability, mySchedule)
# print(good_schedule)
