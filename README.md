# Django User Database Migration

## Overview
    This project demonstrates a successful data migration of  from one custom user model to another custom user model in Django. The migration process involves carefully transferring user data while maintaining data integrity and ensuring a seamless transition from the old schema to the new schema. It also implements the backup of user data.

# Table Of Contents
1. [Datebase Design](#database-design)
2. [Improved User Model(django)](#django-model-user-only)
3. [Installation](#installation)
4. [Steps To migrate data](#step-to-successfull-data-migrations)

# Database Design
    - Old Schema(User)
      - id (pk)
      - username
      - email
      - full_name
      - dob
      - ph number
      - password
    - New Schema (User)
      - id (pk, unique, indexed)
      - username (unique, indexed)
      - email (unique, indexed)
      - full_name (varchar)
      - phone_number
      - password 
      - date_of_birth (indexed)
      - joined_at 
      - updated_at
    - New Schema (Profile)
      - id (pk, indexed)
      - user_id (fk)
      - bio (text field)
      - avatar
      - udpated_at
    - New Address Table
      - id (pk, indexed)
      - user_id (fk)
      - street_address varchar(100)
      - city varchar(100)
      - state varchar(100)
      - postal_code integer(6)
      - country varchar(100)
    - New Schema (Activity)
      - activity_id(pk)
      - user_id int
      - activity_type varchar(100)
      - timestamp timestamp
    - New Schema (Notification)
      - notification_id integer [primary key]
      - message_body varchar(10000)
      - user_id integer
      - is_read bool [default: false]
      - timestamp timestamp

# Django Model (User Only):
    ```
    class NewUser(AbstractBaseUser, PermissionsMixin):
      email: models.EmailField = models.EmailField(max_length=255, unique=True, db_index=True)
      username: models.CharField = models.CharField(max_length=255, unique=True, db_index=True)
      full_name: models.CharField = models.CharField(max_length=255)
      date_of_birth: models.DateField = models.DateField(db_index=True)
      phone_number: models.CharField = PhoneNumberField(region="NP")
      is_active: models.BooleanField = models.BooleanField(default=True)
      is_staff: models.BooleanField = models.BooleanField(default=False)
      joined_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
      updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

      groups = models.ManyToManyField(
          Group,
          related_name="NewUser_set",
          blank=True,
          verbose_name="groups",
          help_text='''The groups this user belongs to. 
                  User will get permissions granted to each of their groups.''',
      )
      user_permissions = models.ManyToManyField(
          Permission,
          related_name='NewUser_set',  # Use a unique related_name
          blank=True,
          verbose_name='user permissions',
          help_text='Specific permissions for this user.',
      )

      # Define the custom user manager
      objects: CustomUserManager = CustomUserManager()

      # Define the field to use as the username for authentication
      USERNAME_FIELD: str = 'username'

      # Define the required fields to use as the username when authenticating
      REQUIRED_FIELDS: list = ['email', 'full_name', 'date_of_birth', 'phone_number']

      def __str__(self) -> str:
          """
          Return the username as a string representation of the user.

          Returns:
              str: The username of the user.
          """
          return f"{self.username}"
    ```

# Installation
  Follow the steps
## Prerequisites
    - A computer/laptop
    - Internet Connection
    - Git (Versioning Tool)
    - Docker (optinal) or else Postgres Database
    - Maketools
    - Python 3.7 or greater

## Clone the Repository
  ```
    git clone https://github.com/ishanshre/DjangoDataMigration.git
  ```

## Environment Configuration
  Create a `.env` file in the project root directory and configure the necessary environment variables, such as database settings and API keys:
  ```
  DJANGO_SECRET=your-secret-key
  DEBUG=True
  db_container_name=new name of database container
  db_username=new database username
  db_password=new database password
  db_dbname=new database name
  db_host=database connection url or hostname or localhost or container ip address i.e. 172.17.0.2 (Only after the database container is created)
  ```

## Create Docker Container
    Run the make file from the root directory

    ```
    make postgresDBContainer
    ```

    Or

    ```
    docker run --name db_container_name -e POSTGRES_USER=db_username -e POSTGRES_PASSWORD=db_password -e POSTGRES_DBNAME=db_dbname -p 5432:5432 -d postgres:latest
    ```

## Populate the db_host in .env file
  ```
  docker inspect your-db-container-name
  ```
  You will find the IP address of container at last. And populate the db_host with it

## Activate the Virutal Environment
  For linux (bash shell):
  ```
  source venv/bin/activate.bash
  ```
  For Windows (powershell):
  ```
  venv\Scripts\activate.bat
  ```

## Install Project Dependencies
```
pip install -r requirements.txt
```

# Step to successfull data migrations:

1. Prerequisites
  - In both table the field must be properly mapped.

2. Comment the NewUser model and Profile model in account app
3. Then Set the User table model in settings.py
   ```AUTH_USER_MODEL = "account.Users"```
4. Remove migration folders in each app
5. Also remove other local apps from the settings
6. Apply makemigrations and migrate
   ```python manage.py makemigrations```
   ```python manage.py migrate```

7. Populate the table with fake. I have created an management command for populating fake data.
   ```python manage.py populate_fake_user_bulk 10000```
8. Now uncomment the NewUser model and Profile model in account.models
9. Run makemigration command
    ```python manage.py makemigrations```
10. Now we will migrate the data from one model to another model. First create a empty migration script
    ```python manage.py makemigrations --empty account```
11. Now we write the data migration script using django migration framework
    ```
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

    ```

12. Now run the migrate command
    ```python manage.py migrate```
13. It will successfully migrate data
14. Now you can the configuration of AUTH_USER_MODEL


# Key Features:
  1. New Optimized Database schema
  2. Custom User model extending Django AbstractBaseUser and PermissionMixin
  3. Backup User data script
  4. Data Migration Script