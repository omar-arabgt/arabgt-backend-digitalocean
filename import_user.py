import os
import csv
import django
from django.db import transaction
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def import_users_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                username = row['username']
                email = row['email']
                nick_name = row['nick_name']
                password = row['password']
                point = int(row['point'])

                get_user_model().objects.create(
                    username = username,
                    email=email,
                    nick_name = nick_name,
                    point = point,
                    password = password,
                )
            except Exception as e:
                print(f"{username} {email} {e}")

    print("Process has been completed")


if __name__ == '__main__':
    file_path = input("Enter CSV file path: ").strip()
    import_users_from_csv(file_path)
