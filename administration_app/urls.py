from django.urls import path
from .views import (
    administration,
    accounts,
    customgroup,
    users,
    superusers,
    support,
    custom_permissions,
)


app_name = "administration_app"

urlpatterns = [
    # ============================== Administration || Dashboard ===================================
    # Administration Dashboard(Future)
    path("dashboard/", administration.admin_view, name="erpadmin"),
    # ============================== Superuser || Account ===================================
    # All superusers List
    path("superusers/", superusers.all_superusers, name="all_superusers"),
    # path('create-superuser/' accounts.create_superuser, name='create_superuser'),
    # ============================== Users || Account ===================================
    path("users/", users.all_users, name="all_users"),  # All Users List.
    # New User Registration
    path("user-register/", users.user_registration, name="user_registration"),
    path("change_user_status/", users.change_user_status, name="change_user_status"),
    path(
        "password-Change/<user_id>/",
        users.user_change_password,
        name="user_change_password",
    ),
    # Users password change (Admin Can Change).
    path("users/delete/<user_id>/", users.delete_user, name="delete_user"),
    # User Account Delete.
    # ============================== Custom Group || Permission ===================================
    path("group/", customgroup.customgroup, name="custom_group"),
    path("add-group/", customgroup.create_custom_group, name="create_custom_group"),
    path(
        "edit-group/<group_id>/",
        customgroup.edit_custom_group,
        name="edit_custom_group",
    ),
    path(
        "delete-group/<group_id>/",
        customgroup.delete_custom_group,
        name="delete_custom_group",
    ),
    path("group/<pk>/", customgroup.customgroup_details, name="customgroup_details"),
    # Custom Group Details
    path(
        "group/<pk>/add-members/",
        customgroup.add_group_members,
        name="add_group_members",
    ),
    # Custom Group Members Add
    path(
        "group/<pk>/remove-members/<member_id>/",
        customgroup.remove_user_from_group,
        name="remove_user_from_group",
    ),
    # Custom Group Members remove
    path(
        "group/<pk>/add-permissions/",
        customgroup.add_permissions,
        name="add_permissions",
    ),
    # Custom Group Permissions Add
    path(
        "group/<pk>/remove-permission/<permission_id>/",
        customgroup.remove_permission_from_group,
        name="remove_permission_from_group",
    ),
    # Custom Group Permissions Remove
    # ============================== Login || Logout ===================================
    path("login/", accounts.user_login, name="user_login"),
    # User Login
    path("logout/", accounts.user_logout, name="user_logout"),
    # User Logout
    # support --------------
    path("support/", support.support, name="support"),
    # Company Support Request.
    path(
        "add-permissions/<int:group_id>/",
        custom_permissions.add_group_permissions,
        name="add_group_permissions",
    ),
]
