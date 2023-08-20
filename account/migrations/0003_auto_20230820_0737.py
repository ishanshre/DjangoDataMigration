"""
Writing custom migration script
"""

from django.db import migrations


def copy_old_user_to_new_and_initite_profile(apps, schema_editor):
    """
    Copies data from the old 'User' model to the new 'NewUser' model.
    Initializes corresponding 'Profile' instances.

    Args:
        apps (object): The application registry.
        schema_editor (object): The schema editor.

    Returns:
        None
    """
    # retrive old and new custom user model as well as profile
    old_user = apps.get_model("account", "User")
    new_user = apps.get_model("account", "NewUser")
    new_user_profile = apps.get_model("account", "Profile")

    # create a list of all users to migrate using bulk migrations
    old_users = old_user.objects.all()
    new_users = [
        new_user(
            email=old_user.email,
            username=old_user.username,
            full_name=old_user.full_name,
            password=old_user.password,
            phone_number=old_user.phone_number,
            date_of_birth=old_user.date_of_birth,
            is_active=old_user.is_active,
            is_staff=old_user.is_staff,
            is_superuser=old_user.is_superuser,
        ) for old_user in old_users
    ]
    new_user.objects.bulk_create(new_users)

    # Instantinate new profile for each users
    profiles = [
        new_user_profile(user=new_user)
        for new_user in new_users
    ]
    new_user_profile.objects.bulk_create(profiles)




class Migration(migrations.Migration):
    """
    Inlcude the custom migrations
    """

    # previous migration file that has not been applied yet
    dependencies = [
        ("account", "0002_newuser_profile"),
    ]

    # deine the custom function
    operations = [
        migrations.RunPython(copy_old_user_to_new_and_initite_profile)
    ]
