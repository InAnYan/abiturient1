from django.db import models


# Абітурієнт.
class Abiturient(models.Model):
    class Sex(models.IntegerChoices):
        MALE = 1, "Чоловік"
        FEMALE = 2, "Жінка"

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    sex = models.PositiveIntegerField(choices=Sex.choices)

    birth_date = models.DateField()
    birth_country = models.CharField(max_length=255)
    birth_town = models.CharField(max_length=255)

    education = models.TextField()

    email = models.EmailField()
    foreign_language = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    work = models.TextField()

    registered_address = models.TextField()
    living_address = models.TextField()


# Член сім'ї.
class FamilyMember(models.Model):
    class Type(models.IntegerChoices):
        MOTHER = 1, "Матір"
        FATHER = 2, "Батько"
        OTHER = 3, "Опікун"

    type = models.IntegerField(choices=Type.choices)

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    telephone = models.CharField(max_length=255)

    abiturient = models.ForeignKey(Abiturient, on_delete=models.CASCADE)


# Телефон.
class Phone(models.Model):
    class Type(models.IntegerChoices):
        HOME = 1, "Домашній"
        MOBILE = 2, "Мобільний"
        WORK = 3, "Робочий"

    type = models.IntegerField(choices=Type.choices)
    number = models.CharField(max_length=255)
    abiturient = models.ForeignKey(Abiturient, on_delete=models.CASCADE)
