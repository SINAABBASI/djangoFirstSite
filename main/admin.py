from django.contrib import admin
from .models import Tutorial,TutorialSeries,TutorialCategory
from django.db import models
from tinymce import TinyMCE
# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
    ## changing order
    # fields = ["tutorial_title",
    #           "tutorial_published",
    #           "tutorial_content"]
    # fieldsets = [
    #     ("title/date", {"fields": ["tutorial_title","tutorial_published"]}),
    #     ("content", {"fields": ["tutorial_content"]})
    # ]
    
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()}
    }

admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial,TutorialAdmin)