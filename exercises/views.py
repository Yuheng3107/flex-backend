from rest_framework.views import APIView, Response
from .models import Exercise, ExerciseStatistics, ExerciseRegime, ExerciseRegimeStatistics, ExerciseSession, ExerciseRegimeInfo
from .serializers import ExerciseRegimeSerializer, ExerciseSerializer, ExerciseStatisticsSerializer, ExerciseRegimeStatisticsSerializer, ExerciseSessionSerializer, ExerciseRegimeInfoSerializer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from feed.views import TagsUpdateView, TagsDeleteView, LikesUpdateView, LikesDeleteView, ShareUpdateView, ShareDeleteView, MediaUpdateView, MediaDeleteView  # type: ignore
from datetime import datetime, timezone
from django.middleware.csrf import get_token
from rest_framework.parsers import FormParser, MultiPartParser
# Create your views here.


class ExerciseUpdateView(APIView):
    def patch(self, request):
        data = request.data
        """To increment staistics to an exercise"""
        """JSON must contain exercise_id in id field"""
        if "id" not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id = data["id"]
        exercise = None
        if "perfect_reps" in data:
            exercise = Exercise.objects.get(pk=id)
            exercise.perfect_reps += data["perfect_reps"]
            exercise.save()
        return Response()


class ExerciseDetailView(APIView):
    """Creation and deletion of an exercise is done in admin console"""
    def get(self, request, pk):
        """To get data for an Exercise instance"""
        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializer(exercise)
            return Response(serializer.data)
        except Exercise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ExerciseRegimeInfoDetailView(APIView):
    # Get the details of an exercise regime (put pk in queryparam in URL)
    def get(self, request, pk):
        """To get data for an Exercise instance"""
        try:
            exerciseRegimeInfo = ExerciseRegimeInfo.objects.filter(exercise_regime=pk)
            serializer = ExerciseRegimeInfoSerializer(exerciseRegimeInfo)
            return Response(serializer.data)
        except ExerciseRegimeInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ExerciseRegimeInfoUpdateView(APIView):
    # Update an exerciseRegime's exercises and reps
    # Takes a PK and three arrays in the body: exercises, set_count, rep_count
    def post(self,request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "id" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            regime = ExerciseRegime.objects.get(pk=request.data["id"])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fields = ["exercises", "rep_count", "set_count"]
        for field in fields:
            if field not in request.data:
                return Response(f"Please add the {field} field in your request", status=status.HTTP_400_BAD_REQUEST)
        if len(request.data["exercises"]) != len(request.data["rep_count"]) or len(request.data["exercises"]) != len(request.data["set_count"]):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for i, exercise in enumerate(request.data["exercises"]):
            try:
                ExerciseRegimeInfo.objects.create(exercise=exercise, exercise_regime=regime.id, rep_count=request.data["rep_count"][i], set_count=request.data["set_count"][i], order=i+1)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()
    
class ExerciseListView(APIView):
    def post(self, request):
        if "exercises" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        exercises = Exercise.objects.filter(pk__in=request.data["exercises"])
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def get(self, request):
        qs = Exercise.objects.all()
        serializer = ExerciseSerializer(qs, many=True)
        return Response(serializer.data)


class ExerciseStatisticsDetailView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        exercise_statistics = ExerciseStatistics.objects.filter(
            exercise=pk).filter(user=request.user.id)
        serializer = ExerciseStatisticsSerializer(exercise_statistics[0])
        return Response(serializer.data)

class ExerciseRegimeStatisticsDetailView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        exercise_regime_statistics = ExerciseRegimeStatistics.objects.filter(
            exercise_regime=pk).filter(user=request.user.id)
        serializer = ExerciseRegimeStatisticsSerializer(exercise_regime_statistics[0])
        return Response(serializer.data)
    
class ExerciseRegimeStatisticsUpdateView(APIView):
    def post(self, request):
        """ To update (increment) exercise regime statistics
            Post request must contain exercise regime foreign key
           It is a post request, not put because it is not idempotent
        """
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response("Please log in", status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        exercise_regime_id = data.get("exercise_regime_id", None)
        if exercise_regime_id is None:
            return Response("Please put exercise_regime_id", status=status.HTTP_400_BAD_REQUEST)
        times_completed = data.get("times_completed", None)
        if times_completed is None:
            return Response("Please put times_completed in the request", status.HTTP_400_BAD_REQUEST)
        try:
            exercise_regime = ExerciseRegime.objects.get(pk=exercise_regime_id)
        except ExerciseRegime.DoesNotExist:
            return Response("Please put a valid exercise_regime id", status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise_regime_statistics = ExerciseRegimeStatistics.objects.get(
                user=request.user, exercise_regime=exercise_regime_id)
        except:
            return Response("Exercise Regime statistics do not exist", status.HTTP_404_NOT_FOUND)
        
        exercise_regime_statistics.times_completed += times_completed
        exercise_regime.times_completed += times_completed
        exercise_regime_statistics.save()
        exercise_regime.save()
        return Response("Successfully Updated")

class ExerciseStatisticsUpdateView(APIView):
    def post(self, request):
        """ To update (increment) exercise statistics
            Post request must contain exercise foreign key
           It is a post request, not put because it is not idempotent
        """
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response("Please log in", status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        exercise_id = data.get("exercise_id", None)
        if exercise_id is None:
            return Response("Please put exercise_id", status=status.HTTP_400_BAD_REQUEST)
        perfect_reps = data.get("perfect_reps", None)
        total_reps = data.get("total_reps", None)
        if perfect_reps is None or total_reps is None:
            return Response("Please put number of perfect reps and total reps done", status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise = Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            return Response("Please put a valid exercise id", status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise_statistics = ExerciseStatistics.objects.get(
                user=request.user.id, exercise=exercise_id)
        except:
            return Response("Exercise statistics do not exist", status.HTTP_404_NOT_FOUND)

        if perfect_reps is not None:
            exercise_statistics.perfect_reps += perfect_reps
            exercise.perfect_reps += perfect_reps
        if total_reps is not None:
            exercise_statistics.total_reps += total_reps
            exercise.total_reps += total_reps
        exercise_statistics.save()
        exercise.save()
        return Response()


class ExerciseStatisticsCreateView(APIView):
    def post(self, request):
        """View for users to send request to create a new exercise statistic, is idempotent
        as .add does not create duplicate entries in through table"""
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response("Please log in.", status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        exercise_id = data.get("exercise_id", None)
        if exercise_id is None:
            return Response("Please put an exercise id", status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise = Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            return Response("Please put a valid exercise id", status=status.HTTP_400_BAD_REQUEST)
        request.user.exercises.add(exercise)
        return Response()


class ExerciseRegimeDetailView(APIView):
    def get(self, request, pk):
        """To get details of an exercise regime"""
        try:
            regime = ExerciseRegime.objects.get(pk=pk)
            serializer = ExerciseRegimeSerializer(regime)
            return Response(serializer.data)
        except ExerciseRegime.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ExerciseRegimeDeleteView(APIView):
    def delete(self, request, pk):
        try:
            regime = ExerciseRegime.objects.get(pk=pk)
            if (regime.poster != request.user):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            regime.delete()
            return Response()
        except ExerciseRegime.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ExerciseRegimeUpdateView(APIView):
    def post(self, request):
        """To update exercise regime"""
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Requires id of exercise_regime
        if "id" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # exercises should not be updated in an exercise regime, otherwise it will break order etc

        # Add new fields to to the fields list for easy maintainance,
        # fields are the fields that we allow the user to update
        # Exercises should not be modifiable so as to not break order

        fields = ["name", "text", "times_completed", "likes"]

        try:
            # Gets exercise regime
            exercise_regime = ExerciseRegime.objects.filter(
                pk=request.data["id"])
            if request.user != exercise_regime[0].poster:
                # Check that person is updating their own post, otherwise kick
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ExerciseRegime.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Only updates fields that are sent in request
        fields = {field: request.data[field]
                  for field in fields if field in request.data}
        exercise_regime.update(**fields)
        # tags is m2m (TODO)
        if "tags" in request.data:
            pass
        # media is base64 encoding that will need to be processed separately (TODO)

        # Linked media also need to handle separately (TODO)

        return Response()


class ExerciseRegimeCreateView(APIView):
    def post(self, request):
        """To create new exercise regime, user needs to be authenticated"""
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # All these fields are required
        fields = ["name", "text", "exercises"]

        # Have to manually do for m2m fields
        # Check that all the required data is in the post request
        for field in fields:
            if field not in request.data:
                return Response(f"Please add the {field} field in your request", status=status.HTTP_400_BAD_REQUEST)

        fields = {field: request.data[field] for field in fields}
        # Unpack the dictionary and pass them as keyword arguments to create in Exercise Regime
        exercise_regime = ExerciseRegime.objects.create(
            poster=request.user, **fields)

        return Response(exercise_regime.id, status=status.HTTP_201_CREATED)


class ExerciseRegimeUpdateImageView(APIView):
    def post(self, request, pk):
        parser_classes = [FormParser, MultiPartParser]

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        uploaded_file_object = request.FILES.get("image", None)
        # Check that image is indeed uploaded
        if uploaded_file_object is None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        """
        file_name = uploaded_file_object.name
        start = file_name.rfind('.')
        allowed_formats = [".png", ".jpeg", ".jpg", ".webp"] 
        if file_name[start:] not in allowed_formats:
            return Response("File format is not allowed",status=status.HTTP_406_NOT_ACCEPTABLE)
        """
        # File size in Megabytes
        file_size = uploaded_file_object.size / (1024*1024)
        if file_size > 2:
            return Response("File size greater than 2MB", status=status.HTTP_400_BAD_REQUEST)

        try:
            exercise_regime = ExerciseRegime.objects.get(pk=pk)
            exercise_regime.media = uploaded_file_object
            exercise_regime.save()
            return Response("Success")
        except:
            return Response("pk does not exist", status.HTTP_400_BAD_REQUEST)


"""
PRESET CLASSES
"""


class ExerciseTagsUpdateView(TagsUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseTagsDeleteView(TagsDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseLikesUpdateView(LikesUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseLikesDeleteView(LikesDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseShareUpdateView(ShareUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseShareDeleteView(ShareDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseMediaUpdateView(MediaUpdateView):
    """Rubbish view"""

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseMediaDeleteView(MediaDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = Exercise


class ExerciseRegimeTagsUpdateView(TagsUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeTagsDeleteView(TagsDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeLikesUpdateView(LikesUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeLikesDeleteView(LikesDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeShareUpdateView(ShareUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeShareDeleteView(ShareDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeMediaUpdateView(MediaUpdateView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class ExerciseRegimeMediaDeleteView(MediaDeleteView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.model = ExerciseRegime


class FavoriteExerciseStatisticView(APIView):
    def post(self, request):
        if "user_id" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        favorite_exercise_stats = ExerciseStatistics.objects.filter(
            user_id=request.data["user_id"]).order_by('-total_reps').first()
        serializer = ExerciseStatisticsSerializer(favorite_exercise_stats)
        return Response(serializer.data)

class ExerciseRegimeStatisticsCreateView(APIView):
    def post(self, request):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        if not request.user.is_authenticated:
            return Response("Please log in.", status=status.HTTP_401_UNAUTHORIZED)
        
        exercise_regime_id = request.data.get("exercise_regime_id", None)
        if exercise_regime_id is None:
            return Response("Please put an exercise_regime id", status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise_regime = ExerciseRegime.objects.get(pk=exercise_regime_id)
        except ExerciseRegime.DoesNotExist:
            return Response("Please put a valid exercise_regime id", status=status.HTTP_400_BAD_REQUEST)
        request.user.exercise_regimes.add(exercise_regime)
        return Response()

class FavoriteExerciseRegimeStatisticView(APIView):
    def post(self, request):
        if "user_id" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        favorite_exercise_regime_stats = ExerciseRegimeStatistics.objects.filter(
            user_id=request.data["user_id"]).order_by('-times_completed').first()
        serializer = ExerciseRegimeStatisticsSerializer(
            favorite_exercise_regime_stats)
        return Response(serializer.data)


class ExerciseSessionCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        required_fields = ["exercise_id", "sets",
                           "duration", "reps", "perfect_reps", "start_time"]
        for field in required_fields:
            if field not in request.data:
                return Response(f"Please add the {field} field in your request", status=status.HTTP_400_BAD_REQUEST)
        # Exercise Regime is optional, if exercise regime id is sent to backend, add it to required fields
        if "exercise_regime" in request.data:
            required_fields.append("exercise_regime")
        # Convert ISO format start time to datetime.datetime object
        request.data["start_time"] = datetime.strptime(
            request.data["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        fields = {field: request.data[field] for field in required_fields}
        ExerciseSession.objects.create(user=request.user, **fields)
        return Response(status=status.HTTP_201_CREATED)


class LatestExerciseSessionView(APIView):
    def post(self, request):
        """Returns 10 most recent exercise sessions, taking into account those the user has already loaded"""
        if "set_no" not in request.data or "user_id" not in request.data:
            return Response(status.HTTP_400_BAD_REQUEST)
        set_no = request.data["set_no"]
        set_size = 10
        start = set_no * set_size
        try:
            exercise_session_qs = ExerciseSession.objects.filter(
                user=request.data["user_id"]).order_by('-id')[start:start+set_size]
            serializer = ExerciseSessionSerializer(
                exercise_session_qs, many=True)
            return Response(serializer.data)
        except:
            return Response("No more exercise sessions", status=status.HTTP_404_NOT_FOUND)
