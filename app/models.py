from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator


class NoInternSpots(Exception):
    pass


# Create your models here.
class Member(models.Model):
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    INTERN, INTERNSUPER, COUNSELOR, GROVE, = \
        'intern', 'internsuper', 'counselor', 'grove',

    member_choices = (
        (INTERN, 'Intern'),
        (INTERNSUPER, 'Organization Supervisor'),
        (COUNSELOR, 'Career / Guidance counselor'),
        (GROVE, 'Grove Employee'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=128, blank=True)
    street = models.CharField(max_length=128, blank=True)
    street2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    zip = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    image = models.ImageField(default='/static/images/default_user.png')
    # Not user controlled
    owning_org = models.ForeignKey('OrgUnit', on_delete=models.SET_NULL, null=True, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    member_type = models.CharField(max_length=36, choices=member_choices, default='Intern')
    email_validated = models.BooleanField(default=False)

    @property
    def is_grove(self):
        return self.member_type == self.GROVE

    @property
    def is_student(self):
        return self.member_type == self.INTERN

    @property
    def is_supervisor(self):
        return self.member_type == self.INTERNSUPER

    @property
    def is_counselor(self):
        return self.member_type == self.COUNSELOR


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()


class OrgUnit(models.Model):
    def __str__(self):
        return self.org_name + ' - ' + self.country

    ENTERPRISE, NONPROF, PRIMEDU, HIGHEDU, OTHER, = \
        'enterprise', 'nonprofit', 'primaryeducation', 'secondaryeducation', 'other',

    org_choices = (
        (ENTERPRISE, 'Enterprise'),
        (NONPROF, 'Non-Profit'),
        (PRIMEDU, 'Primary Education / K-12'),
        (HIGHEDU, 'Secondary / Higher Education'),
        (OTHER, 'Other'),
    )

    org_name = models.CharField(max_length=128, unique=True)
    org_type = models.CharField(max_length=36, choices=org_choices, default='Other')
    street = models.CharField(max_length=128, blank=True)
    street2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    zip = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    industry = models.CharField(max_length=128, default='Unknown')
    bio = models.TextField(max_length=500, blank=True)
    logo = models.ImageField(default='/static/images/default_company.png')
    website = models.URLField(default=None, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    intern_limit = models.IntegerField(default=0)


class Internship(models.Model):
    def __str__(self):
        return self.company.org_name + ' ' + self.title

    company = models.ForeignKey(OrgUnit)
    main_contact = models.ForeignKey(User)  # where member_type is INTERNSUPER or ORGMAIN and company above
    #    supervisor = models.ForeignKey(Member) Where member_type is INTERNSUPER and company above
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=640)
    openings = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)


class InternApplication(models.Model):
    SUBMITTED, PENDING, APPROVED, DENIED, NEEDSCLARIFICATION, WAITLIST = \
        'submitted', 'pending', 'approved', 'denied', 'needsclarification', 'waitlist'

    state_choices = (
        (SUBMITTED, 'Application Submitted'),
        (PENDING, 'Application Pending Review'),
        (APPROVED, 'Application Approved'),
        (DENIED, 'Application Denied'),
        (NEEDSCLARIFICATION, 'Application Needs Clarification'),
        (WAITLIST, 'Application Waitlisted')
    )
    internship = models.ForeignKey(Internship)
    applicant = models.ForeignKey(User, related_name='Application_Interns')  # Where member_type is INTERN
    letter = models.TextField(max_length=500, blank=True)
    notes = models.TextField(max_length=500, blank=True)
    state = models.CharField(max_length=36, choices=state_choices, default='submitted')
    date_created = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=InternApplication)
def approve_or_waitlist(sender, instance, **kwargs):
    perform_license_check = False
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        if instance.state == InternApplication.APPROVED:
            perform_license_check = True
            # pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if instance.state == InternApplication.APPROVED and obj.state != InternApplication.APPROVED:
            perform_license_check = True

    if perform_license_check == True:
        today = now()
        org_info = instance.internship.company
        spots_filled = InternApplication.objects.filter(internship__company=org_info,
                                                        internship__start_date__lte=today,
                                                        internship__end_date__gte=today,
                                                        state='approved').count()
        if spots_filled > org_info.intern_limit:
            print('no openings')
            raise NoInternSpots
        print(spots_filled)
        # spots = internship_info.openings - application_info.filter(state='approved').count()


class InternshipTask(models.Model):
    def __str__(self):
        return self.name

    internship = models.ForeignKey(Internship)
    name = models.CharField(max_length=128)
    details = models.TextField(max_length=640)
    estimation = models.DurationField()
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_question_update = models.DateTimeField(null=True, blank=True)


class InternshipTaskQuestion(models.Model):
    def __str__(self):
        return self.question + ' from ' + self.task.name + ' by ' + self.author.username

    author = models.ForeignKey(User)
    task = models.ForeignKey(InternshipTask, related_name='questions')
    question = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(InternshipTaskQuestion, self).save(*args, **kwargs)
        self.task.date_last_question_update = now()
        self.task.save()


class InternshipTaskAnswer(models.Model):
    def __str__(self):
        return self.answer + self.intern.first_name + self.intern.last_name

    answer = models.CharField(max_length=128)
    question = models.ForeignKey(InternshipTaskQuestion, related_name='answers')
    intern = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)


class InternshipTaskProgress(models.Model):
    def __str__(self):
        return self.intern.first_name + self.task.name

    p024, p25, p2649, p50, p5174, p75, p7699, p100 = \
        0, 25, 37, 50, 62, 75, 87, 100
    progress_choices = (
        (p024, '0-25%'),
        (p25, '25%'),
        (p2649, '25-50%'),
        (p50, '50%'),
        (p5174, '50-75%'),
        (p75, '75%'),
        (p7699, '70-99%'),
        (p100, '100% Complete'),
    )

    intern = models.ForeignKey(User)
    task = models.ForeignKey(InternshipTask, related_name='progress')
    time_stamp = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=50, choices=progress_choices)


class InternshipTaskEndQuestion(models.Model):
    def __str__(self):
        return self.question

    active = models.BooleanField(default=True)
    question = models.TextField()
    order = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)


class InternshipTaskEndAnswers(models.Model):
    def __str__(self):
        return self.task.name + self.intern.username

    task = models.ForeignKey(InternshipTask)
    intern = models.ForeignKey(User)
    question = models.ForeignKey(InternshipTaskEndQuestion)
    date_created = models.DateTimeField(auto_now_add=True)
    answer = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1.0), MaxValueValidator(10.0), ])
    text = models.TextField(default='Type your feedback for the supervisor here.', max_length=640)


class InternshipFocus(models.Model):
    def __str__(self):
        return self.text + ' for ' + self.internship.title

    internship = models.ForeignKey(Internship, related_name='focus')
    length = models.DurationField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    text = models.TextField(max_length=640)


class InternshipFocusEndAnswers(models.Model):
    def __str__(self):
        return self.intern.username + ' for ' + self.focus.internship.title

    focus = models.ForeignKey(InternshipFocus, related_name='focus_answers')
    intern = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(max_length=640)


class PerformanceFeedback(models.Model):
    def __str__(self):
        return self.question + ' for ' + self.internship.title

    internship = models.ForeignKey(Internship, related_name='feedback')
    author = models.ForeignKey(User)
    question = models.TextField(max_length=120)
    date_created = models.DateTimeField(auto_now_add=True)


class PerformanceFeedbackAnswers(models.Model):
    def __str__(self):
        return self.supervisor.username + ' for ' + self.feedback.title

    feedback = models.ForeignKey(PerformanceFeedback, related_name='feedback_answers')
    supervisor = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(max_length=640)


class Resources(models.Model):
    def __str__(self):
        return self.state + self.type + 'by' + self.author.username

    SUBMITTED, PENDING, APPROVED, ISSUE, DENIED, DISABLED = \
        'enabled', 'pending', 'approved', 'issue', 'denied', 'disabled'

    state_choices = (
        (SUBMITTED, 'Submitted'),
        (PENDING, 'Pending Review'),
        (APPROVED, 'Approved'),
        (ISSUE, 'Issue or Complaint'),
        (DENIED, 'Denied'),
        (DISABLED, 'Disabled')
    )

    URL, TEXT, SOCIAL, OTHER, = \
        'url', 'txt', 'social', 'other'

    type_choices = (
        (URL, 'url'),
        (TEXT, 'Text'),
        (SOCIAL, 'Social Networking Handel'),
        (OTHER, 'Other'),
    )
    author = models.ForeignKey(User)
    state = models.CharField(max_length=36, choices=state_choices, default='submitted')
    type = models.CharField(max_length=36, choices=type_choices, default='text')
    url = models.URLField(default=None, blank=True)
    text = models.TextField(max_length=640, blank=True)
    social = models.CharField(max_length=36, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Counselor(models.Model):
    """
    The Connection between a Counselor and school.
    A relation here means that a student's info will show in school view.

    """

    def __str__(self):
        return self.counselor.first_name + ' for ' + self.school.org_name

    counselor = models.ForeignKey(User, related_name='org_counselor')
    school = models.ForeignKey(OrgUnit)


class SchoolGroups(models.Model):
    """
    The Connection between a student/intern and a school.
    A relation here means that a student's info will show in school view.

    """

    def __str__(self):
        return self.intern.first_name + ' at ' + self.school.org_name

    school = models.ForeignKey(OrgUnit)
    intern = models.ForeignKey(User, related_name='org_intern')
    counselor_view_permission = models.BooleanField(default=True)

