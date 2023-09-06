from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .renderers import UserJSONRenderer
import requests
from datetime import datetime
import holidays
import asyncio
from .backend import JWTAuthentication

# Create your views here.
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer
)




auth = JWTAuthentication()

class RegistrationAPIView(CreateAPIView):
    """
    Register a new user.
    """
    # Allow any user (authenticated or not) to hit thiis endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        request.data['username'] = request.data['username'].lower()
        user = request.data
        # Get the user's IP address from the request
        # user_ip = request.META.get('REMOTE_ADDR')
        
        user_ip='196.216.242.131'
        # Use the ipinfo.io API to determine the user's country
        response = requests.get(f'https://ipinfo.io/{user_ip}/json')
        data = response.json()
        user_country = data.get('country')
        # import pdb;pdb.set_trace()

        # Get the list of holidays for the user's country
        try:
            holiday_list = holidays.CountryHoliday(user_country)
        except holidays.UnknownCountryError:
            holiday_list = None
        
        # Check if the signup date is a holiday
        signup_date = datetime.now().date()  # You can replace this with the actual signup date
        is_holiday = False
        

        if holiday_list:
            is_holiday = signup_date in holiday_list

        # Save the signup information along with the holiday status
        # Replace this with your actual signup data saving logic
        # Example: user = User.objects.create(username=username, ...)
        
        # Return a response indicating whether it's a holiday
        # Return a response indicating whether it's a holiday
        # serializer = self.serializer_class(
        #     data=user, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # success_message={
        #     "success": "Please check your email for a link to complete your registration!"
        # }
        # return Response(success_message, status=status.HTTP_201_CREATED)
        #     return Response({'message': 'Signup successful', 'is_holiday': is_holiday})
        # return Response({'message': 'Invalid request method'}, status=400)

        serializer = self.serializer_class(
            data=user, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        success_message={
            "success": "Signup successful",
            'is_holiday': is_holiday
        }
        return Response(success_message, status=status.HTTP_201_CREATED)

class LoginAPIView(CreateAPIView):
    """
    Login a registered user asynchronously.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        """Retrieve user details asynchronously"""
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
