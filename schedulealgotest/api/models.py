from django.db import models
import datetime


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Student(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["last_name"]


class TimeSlot(models.Model):
    day_choices = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    )

    start_time_choices = (
        (datetime.time(10, 0, 0), "10:00 AM"),
        (datetime.time(12, 15, 0), "12:15 PM"),
        (datetime.time(14, 30, 0), "2:30 PM"),
    )

    end_time_choices = (
        (datetime.time(12, 00, 0), "12:00 PM"),
        (datetime.time(2, 15, 0), "2:15 PM"),
        (datetime.time(16, 30, 0), "4:30 PM"),
    )

    day = models.CharField(max_length=10, choices=day_choices)
    start_time = models.TimeField(choices=start_time_choices)
    end_time = models.TimeField(choices=end_time_choices)

    def __str__(self):
        return self.day + " " + str(self.start_time) + "-" + str(self.end_time)

    class Meta:
        ordering = ["day"]


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subjects = models.ManyToManyField(Subject)
    availability = models.ManyToManyField(TimeSlot)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["last_name"]


class reoccuringApp(models.Model):

    day_choices = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),

    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    time_slot = models.ManyToManyField(TimeSlot)

    def __str__(self):
        return (
            self.student.first_name
            + "/"
            + self.student.last_name[0]
            + "./"
            + self.subject.name
            + "/"
            + self.time_slot.all()[0].day
            + "/"
            + self.time_slot.all()[0].start_time.strftime("%I:%M %p")
            + "-"
            + self.time_slot.all()[0].end_time.strftime("%I:%M %p")
        )

class appInstance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=50, null=True, blank=True, default="unconfirmed"
    )

    class Meta:
        ordering = ["student", "date", "time"]

    def __str__(self):
        return (
            self.student.first_name
            + " "
            + self.student.last_name
            + " "
            + self.subject.name
            + " "
            + self.date.strftime("%Y-%m-%d")
        )
