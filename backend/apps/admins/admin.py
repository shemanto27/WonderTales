from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AppDetailsModel, ReportModel

@admin.register(AppDetailsModel)
class AppDetailsAdmin(ModelAdmin):
    list_display = ["__str__"]
    
@admin.register(ReportModel)
class ReportAdmin(ModelAdmin):
    list_display = ["reporter", "target_type", "target_id", "created_at"]
    list_filter = ["target_type", "created_at"]
    search_fields = ["reporter__email", "target_id", "reason"]