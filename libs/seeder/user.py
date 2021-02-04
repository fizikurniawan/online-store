from django.contrib.auth.models import User


def generate_superuser():
    user = User.objects.filter(email='superuser@user.com').last()
    if not user:
        user = User.objects.create(
            first_name='Super User',
            last_name='Admin',
            email='superuser@user.com',
            is_superuser=True,
            is_active=True
        )

    user.set_password('superuser')


def generate_user():
    user = User.objects.filter(email='user@user.com').last()
    if not user:
        user = User.objects.create(
            first_name='User',
            last_name='Basic',
            email='basic@user.com',
            is_superuser=False,
            is_active=True
        )

    user.set_password('basic')
