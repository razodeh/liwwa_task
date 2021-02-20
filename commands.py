import click
from flask.cli import with_appcontext

from exceptions import TinyHRError
from services.user_service import UserService
from utils import is_valid_email, is_valid_password


def valid_email(ctx, param, value):
    if not is_valid_email(value):
        raise click.BadParameter('Invalid Email Address.')
    return value


def valid_password(ctx, param, value):
    if not is_valid_password(value):
        raise click.BadParameter('Invalid Password, it should be at leas 8 characters.')
    return value


@click.command('create_admin')
@click.option('--first_name', prompt="First Name")
@click.option('--last_name', prompt="Last Name")
@click.option('--email', prompt="Email", callback=valid_email)
@click.option('--password', prompt="Password", callback=valid_password)
@with_appcontext
def create_admin(first_name, last_name, email, password):
    try:
        UserService().create(user_details={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }, is_admin=True)
        print(f"User '{email}' was created successfully.")
    except TinyHRError:
        print(f"User with email ({email}) already exists")
