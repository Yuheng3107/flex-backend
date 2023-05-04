from rest_framework import serializers
from .models import ExerciseRegime, Exercise, ExerciseRegimeStatistics, ExerciseStatistics, ExerciseSession, ExerciseRegimeInfo

class ExerciseRegimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRegime
        fields = '__all__'
        
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        
class ExerciseStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseStatistics
        exclude = ['user', 'id']
        
class ExerciseRegimeStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRegimeStatistics
        exclude = ['user', 'id']
        
class ExerciseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSession
        fields = '__all__'

class ExerciseRegimeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRegimeInfo
        fields = '__all__'