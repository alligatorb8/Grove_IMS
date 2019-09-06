from django.contrib import admin
from .models import *


# Register your models here.
class InternMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'country', ]


admin.site.register(Member, InternMemberAdmin)


class CompanyUnitAdmin(admin.ModelAdmin):
    list_display = ['org_name', 'intern_limit', 'city', 'state', 'country', ]


admin.site.register(OrgUnit, CompanyUnitAdmin)


# class CompanyMemberAdmin(admin.ModelAdmin):
#    list_display = ['first_name', 'last_name', 'company', 'country', ]


# admin.site.register(CompanyMember, CompanyMemberAdmin)


class InternshipAdmin(admin.ModelAdmin):
    list_display = ['company', 'title', 'main_contact', 'registration_start_date', 'end_date', ]


admin.site.register(Internship, InternshipAdmin)


class InternshipTaskAdmin(admin.ModelAdmin):
    list_display = ['internship', 'name', 'estimation', ]


admin.site.register(InternshipTask, InternshipTaskAdmin)


class InternshipTaskQuestionAdmin(admin.ModelAdmin):
    list_display = ['task', 'question', ]


admin.site.register(InternshipTaskQuestion, InternshipTaskQuestionAdmin)


class InternshipTaskAnswerAdmin(admin.ModelAdmin):
    list_display = ['intern', 'question', 'answer', ]


admin.site.register(InternshipTaskAnswer, InternshipTaskAnswerAdmin)


class InternshipTaskProgressAdmin(admin.ModelAdmin):
    list_display = ['task', 'intern', 'time_stamp', 'progress', ]


admin.site.register(InternshipTaskProgress, InternshipTaskProgressAdmin)


class InternApplicationAdmin(admin.ModelAdmin):
    list_display = ['internship', 'applicant', 'letter', 'date_created', 'state', ]


admin.site.register(InternApplication, InternApplicationAdmin)


class InternshipTaskEndQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'active', 'order', 'date_created']


admin.site.register(InternshipTaskEndQuestion, InternshipTaskEndQuestionAdmin)


class InternshipTaskEndAnswersAdmin(admin.ModelAdmin):
    list_display = ['task', 'intern', 'question', 'answer']


admin.site.register(InternshipTaskEndAnswers, InternshipTaskEndAnswersAdmin)


class InternshipFocusAdmin(admin.ModelAdmin):
    list_display = ['internship', 'date_created', 'author']


admin.site.register(InternshipFocus, InternshipFocusAdmin)


class InternshipFocusEndAnswersAdmin(admin.ModelAdmin):
    list_display = ['intern', 'focus', 'date_created', 'answer']


admin.site.register(InternshipFocusEndAnswers, InternshipFocusEndAnswersAdmin)

class InternshipFeedbackAdmin(admin.ModelAdmin):
    list_display = ['internship', 'date_created', 'author']


admin.site.register(PerformanceFeedback, InternshipFeedbackAdmin)


class InternshipFeedbackAnswersAdmin(admin.ModelAdmin):
    list_display = ['supervisor', 'feedback', 'date_created', 'answer']


admin.site.register(PerformanceFeedbackAnswers, InternshipFeedbackAnswersAdmin)


class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['type', 'state', 'date_created', 'author']


admin.site.register(Resources, ResourcesAdmin)


class CounselorAdmin(admin.ModelAdmin):
    list_display = ['counselor', 'school', ]


admin.site.register(Counselor, CounselorAdmin)


class SchoolGroupsAdmin(admin.ModelAdmin):
    list_display = ['intern', 'school', ]


admin.site.register(SchoolGroups, SchoolGroupsAdmin)
