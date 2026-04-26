from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import CustomUserModel, ChildrenProfileModel
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

class ChildrenProfileInline(TabularInline):
    model = ChildrenProfileModel
    extra = 0

@admin.register(CustomUserModel)
class UserAdmin(ModelAdmin):
    list_display = ["email", "username", "is_active", "is_email_verified", "date_joined"]
    list_filter = ["is_active", "is_email_verified", "is_staff"]
    search_fields = ["email", "username"]
    inlines = [ChildrenProfileInline]
    
    def changelist_view(self, request, extra_context=None):
        """Override to add chart data to the user list page"""
        extra_context = extra_context or {}
        
        # Calculate user statistics
        total_users = CustomUserModel.objects.count()
        active_users = CustomUserModel.objects.filter(is_active=True).count()
        inactive_users = CustomUserModel.objects.filter(is_active=False).count()
        verified_users = CustomUserModel.objects.filter(is_email_verified=True).count()
        
        extra_context.update({
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "verified_users": verified_users,
        })
        
        # Chart data
        try:
            data = (
                CustomUserModel.objects
                .annotate(date=TruncDay("date_joined"))
                .values("date")
                .annotate(count=Count("id"))
                .order_by("date")
            )
            
            labels = [d["date"].strftime("%Y-%m-%d") for d in data] if data else []
            values = [d["count"] for d in data] if data else []
        except Exception:
            labels = []
            values = []
        
        chart_data = {
            "labels": labels,
            "datasets": [{
                "label": "New Users",
                "data": values,
                "borderColor": "#7c3aed", 
                "backgroundColor": "rgba(124, 58, 237, 0.1)",
                "tension": 0.4,
                "fill": True
            }],
        }
        
        extra_context["user_growth_chart"] = json.dumps(chart_data)
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ChildrenProfileModel)
class ChildrenProfileAdmin(ModelAdmin):
    list_display = ["child_name", "user", "child_age", "child_gender", "created_at"]
    list_filter = ["child_gender", "created_at"]
    search_fields = ["child_name", "user__email"]

# Unfold Dashboard Stats
def user_stats_callback(request, context):
    context.update({
        "total_users": CustomUserModel.objects.count(),
        "active_users": CustomUserModel.objects.filter(is_active=True).count(),
        "total_children": Children_Profile.objects.count(),
    })

    try:
        data = (
            CustomUserModel.objects
            .annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        labels = [d["date"].strftime("%Y-%m-%d") for d in data] if data else []
        values = [d["count"] for d in data] if data else []
        
        chart_data = {
            "labels": labels,
            "datasets": [{
                "label": "New Users",
                "data": values,
                "borderColor": "#7c3aed", 
                "backgroundColor": "rgba(124, 58, 237, 0.1)",
                "tension": 0.4,
                "fill": True
            }],
        }
        context["dashboard_chart"] = json.dumps(chart_data)
    except Exception as e:
        context["dashboard_chart"] = json.dumps({"labels": [], "datasets": []})

    return context