from django.db.models import IntegerChoices


class StaffLevel(IntegerChoices):
    USER = 0, 'User'
    INTERN = 1, 'Intern'
    JUNIOR = 2, 'Junior'
    MID = 3, 'Mid'
    SENIOR = 4, 'Senior'
    MANAGER = 5, 'Manager'
