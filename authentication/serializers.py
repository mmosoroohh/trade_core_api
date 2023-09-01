from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer registration requests and creates a new user.
    """
    # Ensure passwords are atleast * characters long, no longer than 128
    # characters and can not be read by the client.
    password = serializers.RegexField(
        regex="^(?=.*\d).{8,20}$",
        max_length=128,
        min_length=6,
        write_only=True,
        required=True,
        error_messages={
            'required': 'Sorry, Password is required!',
            'invlaid': 'Sorry, Passwords must contain a letter and a number!',
            'min_length': 'Sorry, Password must contain atleast 6 characters!',
            'max_length': 'Sorry, Password cannot contain more than 128 characters!'
        }
    )

    # Ensure username is unique
    username = serializers.RegexField(
        regex="^(?!.*\ )[A-Za-z\d\-\_][^\W_]+$",
        min_length=3,
        required=True,
        validators = [
            UniqueValidator(
                queryset=User.objects.all(),
                message="Sorry, this username is already taken!"
            )
        ],
        error_messages= {
            'invalid': 'Sorry, invalid username. No spaces or special characters allowed!'
            'required': 'Sorry, username is required!'
            'min_length': 'Sorry, username must have atleast 3 characters!'
        }
    )

    # ensure email is unique
    email = serializers.RegexField(
        regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Sorry, this email is already in user!',
            )
        ],
        error_messages={
            'required': 'Sorry, an email address is required!',
            'invalid': 'Sorry, please provide a valid email address!'
        }
    )
    token = serializers.CharField(
        read_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user
        user = User.objects.create_user(**validated_data)
        return user 


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in!'
            ) 

        # As mentioned above, a password is required. Raise an exception if a 
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in!'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found!'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated!'
            )

        if not user.is_activated:
            raise serializers.ValidationError(
                'To login, Please check your email for a link to complete your registration!'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of User object.
    """
    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.RegexField(
        regex="^(?=.*\d).{8,20}$",
        max_length=128,
        min_length=6,
        write_only=True,
        required=True,
        error_messages={
            'invalid': 'Sorry, passwords must contain a letter and a number!',
            'min_length': 'Sorry, passwords must contain atleast 6 characters!',
            'max_length': 'Sorry, passwords cannot contain more than 128 characters!'
        }
    )

    email = serializers.RegexField(
        regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        required=False,
        error_messages={
            'invalid': 'Sorry, please enter a valid email address!'
        }
    )

    class Meta:
        model = User
        fields = ('email', 'password')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

        def update(self, instance, validated_data):
            # Passwords should not be handled with `setattr`, unlike other fields.
            # This is because Django provides a function that handles hashing and
            # salting passwords, which is important for security. What that means
            # here is that we need to remove the password field from the
            # `validated_data` dictionary before iterating over it.
            password = validated_data.pop('password', None)

            for(key, value) in validated_data.items():
                # For the keys remaining in `validated_data`, we will set them on
                # the current `User` instance one at a time.
                setattr(instance, key, value)

            # Finally, after everything has been updated, we must explicitly save
            # the model. It's worth pointing out that `.set_password()` does not
            # save the model.
            instance.save()

            return instance

        def get_user(self, email=None, username=None, id=None):
            try:
                if email:
                    user = User.objects.get(email=email)
                elif username:
                    user = User.objects.get(username=username)
                else:
                    user = User.objects.get(id=id)
                return user 
            except User.DoesNotExist:
                raise serializers.ValidationError("Sorry, that email account is not registered on Trade Core")
