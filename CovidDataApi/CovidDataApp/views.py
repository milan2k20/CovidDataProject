from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from CovidDataApp.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from CovidDataApp.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from CovidDataApp.validation import validate_input
import requests
from datetime import datetime


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserDataView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        base_url = 'http://corona-api.com/countries/'
        data = validate_input(request)
        try:            
            if data['errorMessage'] == '':
                resp = requests.get(base_url + data['country'])
                result = resp.json()
                timeline = result.get('data').get('timeline')

                filtered_timeline = []
                latest_date = datetime.strptime(timeline[0]['date'], "%Y-%m-%d")
                start_index = (latest_date - datetime.strptime(data['endDate'], "%Y-%m-%d")).days
                end_index = start_index + int(data['difference'])
                
                for index in range(start_index, end_index):
                    filtered_timeline.append(timeline[index])
                result['data']['timeline'] = filtered_timeline
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(data['errorMessage'],status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:            
            return Response('Exception occurred while fetching data.',status = status.HTTP_500_INTERNAL_SERVER_ERROR)

