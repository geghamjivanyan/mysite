from django.contrib import admin

# Register your models here.
from .models import Question, Choice, PollUser, UserLog

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main information", {"fields": ["question_text"], "classes": ["collapse"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ["id", "question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class PollUserAdmin(admin.ModelAdmin):
    list_display = ["id", "get_full_name", "country"]
    list_filter = ["user__is_superuser"]

    def get_full_name(self, obj):
        return "{} {}".format(obj.user.first_name, obj.user.last_name)
    get_full_name.short_description = "Full Name"

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(PollUser, PollUserAdmin)
admin.site.register(UserLog)