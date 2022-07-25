from rest_framework import serializers

from .models import Student, Teacher, Subject, appInstance, reoccuringApp


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class appInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = appInstance
        fields = "__all__"


class ReoccuringAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = reoccuringApp
        fields = "__all__"
