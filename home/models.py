from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
class TutoringUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_tutor = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    MAJOR_CHOICES = [
        ('AE', 'Aerospace Engineering'),
        ('AAS', 'African American and African Studies'),
        ('AMST', 'American Studies'),
        ('ANTH', 'Anthropology'),
        ('ARCY', 'Archaeology'),
        ('ARH', 'Architectural History'),
        ('ARCH', 'Architecture'),
        ('ASTR', 'Astronomy'),
        ('IDST', 'Bachelor of Interdisciplinary Studies'),
        ('HSM', 'Bachelor of Professional Studies in Health Sciences Management'),
        ('BIOL', 'Biology'),
        ('BME', 'Biomedical Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('CHEM', 'Chemistry'),
        ('CE', 'Civil Engineering'),
        ('CLAS', 'Classics'),
        ('COGS', 'Cognitive Science'),
        ('COMM', 'Commerce'),
        ('CPL', 'Comparative Literature'),
        ('CPE', 'Computer Engineering'),
        ('CS', 'Computer Science (B.A.)'),
        # ('', 'Computer Science (B.S.)'),
        ('DANC', 'Dance'),
        ('DRAM', 'Drama'),
        ('ECED', 'Early Childhood Education (BSEd)'),
        ('EALC', 'East Asian Languages, Literatures and Culture'),
        ('ECON', 'Economics'),
        ('ELE', 'Electrical Engineering'),
        ('ELED', 'Elementary Education (BSEd)'),
        ('ES', 'Engineering Science'),
        ('ENGL', 'English'),
        ('EVCS', 'Environmental Sciences'),
        ('ETP', 'Environmental Thought and Practice'),
        ('FREN', 'French'),
        ('GERM', 'German'),
        ('GETR', 'German Studies'),
        # ('', 'Global Studies'),
        # ('', 'Global Sustainability Minor'),
        # ('', 'Historic Preservation Minor'),
        ('HIST', 'History'),
        ('ARTH', 'History of Art'),
        ('HBIO', 'Human Biology'),
        # ('', 'Interdisciplinary Major of Global Studies'),
        ('JEST', 'Jewish Studies'),
        ('KINE', 'Kinesiology (BSEd)'),
        # ('LAR', 'Landscape Architecture Minor'),
        ('LAST', 'Latin American Studies'),
        ('LING', 'Linguistics'),
        ('MSE', 'Materials Science and Engineering'),
        ('MATH', 'Mathematics'),
        ('ME', 'Mechanical Engineering'),
        ('MDST', 'Media Studies'),
        ('MSP', 'Medieval Studies'),
        ('MESA', 'Middle Eastern and South Asian Languages and Cultures'),
        ('MUSI', 'Music'),
        ('NESC', 'Neuroscience'),
        ('NURS', 'Nursing'),
        ('PHIL', 'Philosophy'),
        ('PHYS', 'Physics'),
        ('PST', 'Political and Social Thought'),
        ('PPL', 'Political Philosophy, Policy, and Law'),
        ('PL', 'Politics'),
        ('PSYC', 'Psychology'),
        ('RELG', 'Religious Studies'),
        ('SLAV', 'Slavic Languages and Literatures'),
        ('SOC', 'Sociology'),
        ('SPAN', 'Spanish'),
        ('SPED', 'Special Education (BSEd)'),
        ('SCD', 'Speech Communication Disorders'),
        ('STAT', 'Statistics'),
        ('ARTS', 'Studio Art'),
        ('SYS', 'Systems Engineering'),
        ('PLAN', 'Urban and Environmental Planning'),
        ('WGS', 'Women, Gender & Sexuality'),
        ('YSI', 'Youth & Social Innovation (BSEd)')
    ]
    def get_default():
        return list()
    major = models.CharField(max_length=4, choices=MAJOR_CHOICES)
    locations = ArrayField(models.CharField(max_length=20, default="NA"), default=get_default)
    is_virtual = models.BooleanField(default=False)
    classes = ArrayField(models.CharField(max_length=50, default="NA"), default=get_default)
    availability = ArrayField(models.CharField(max_length=255, default="NA"), default=get_default)
    pay_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tutorSession = ArrayField(
        models.JSONField(encoder=DjangoJSONEncoder),
       default=get_default,
        blank=True,
        null=True
    )

    def set_availability(self, availabilities):
        self.tutorSession = availabilities

    def get_availability(self):
        return self.tutorSession

    def add_availability(self,date):
        self.tutorSession.append(date)

    def remove_availability(self, date):
        self.tutorSession.remove(date)

class TutorRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_requests')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_requests')
    session_date = models.DateField()
    session_time = models.TimeField()
    duration= models.DecimalField(max_digits=5, decimal_places=2,default=0)
    description= models.CharField(max_length=255, null=True)
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    
