from tutor.models import Event, Instructor, Student
from rest_framework import serializers


# class DtField(serializers.RelatedField):
#     def to_native(self, value):
#         duration = time.strftime('%M:%S', time.gmtime(value.duration))
#         return 'Track %d: %s (%s)' % (value.order, value.name, duration)

class TutorEventsSerializer(serializers.ModelSerializer):

    student = serializers.CharField(source='student.__str__', read_only=True)
    instructor = serializers.CharField(source='instructor.name', read_only=True)
    dt = serializers.CharField(source='get_date', read_only=True)
    dt_type = serializers.CharField(source='get_date_type', read_only=True)
    from_to_time = serializers.CharField(source='get_from_to_time', read_only=True)

    class Meta:
        model = Event
        fields = ('dt', 'instructor', 'student', 'dt_type','from_to_time')
