from bible_study.models import DashboardCard, Question, Scripture
from rest_framework import serializers

class AnnouncementSerializer(serializers.ModelSerializer):

    title =  serializers.CharField(read_only=True)
    msg_text = serializers.CharField(source='get_api_announcement_text', read_only=True)

    class Meta:
        model = DashboardCard
        fields = ('title','msg_text',)

class QuestionSerializer(serializers.ModelSerializer):

    # question = serializers.CharField(source='question', read_only=True)
    questions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='question'
     )

    title =  serializers.CharField(read_only=True)
    passage  =  serializers.CharField(source='get_passage_api', read_only=True)
    key_verse = serializers.CharField(source='get_key_verse_text', read_only=True)

    class Meta:
        model = Scripture
        fields = ('title','passage','key_verse','questions',)

class PrayerTopicSerializer(serializers.ModelSerializer):

    msg_text = serializers.CharField(source='get_api_prayer_topic_text', read_only=True)
    title =  serializers.CharField(read_only=True)

    class Meta:
        model = DashboardCard
        fields = ('title','msg_text',)
