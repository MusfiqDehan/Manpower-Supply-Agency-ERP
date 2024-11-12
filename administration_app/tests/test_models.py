import pytest
from django.contrib.auth.hashers import check_password
from ..models import PermissionApp, Permissions, User, CustomGroup


@pytest.mark.django_db
def test_create_edit_delete_permission_app():
    # Create
    permission_app = PermissionApp.objects.create(name="App1")
    assert PermissionApp.objects.count() == 1

    # Edit
    permission_app.name = "App2"
    permission_app.save()
    permission_app.refresh_from_db()
    assert permission_app.name == "App2"

    # Delete
    permission_app.delete()
    assert PermissionApp.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_permissions():
    permission_app = PermissionApp.objects.create(name="App1")

    # Create
    permission = Permissions.objects.create(
        name="Permission1", codename="perm1", permission_app=permission_app
    )
    assert Permissions.objects.count() == 1

    # Edit
    permission.name = "Permission2"
    permission.save()
    permission.refresh_from_db()
    assert permission.name == "Permission2"

    # Delete
    permission.delete()
    assert Permissions.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_user():
    # Create
    user = User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )
    assert User.objects.count() == 1
    assert check_password("password123", user.password)

    # Edit
    user.first_name = "Jane"
    user.save()
    user.refresh_from_db()
    assert user.first_name == "Jane"

    # Delete
    user.delete()
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_custom_group():
    user = User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )
    permission_app = PermissionApp.objects.create(name="App1")
    permission = Permissions.objects.create(
        name="Permission1", codename="perm1", permission_app=permission_app
    )

    # Create
    group = CustomGroup.objects.create(name="Group1", description="Test group")
    group.permissions.add(permission)
    group.group_users.add(user)
    assert CustomGroup.objects.count() == 1
    assert group.permissions.count() == 1
    assert group.group_users.count() == 1

    # Edit
    group.name = "Group2"
    group.save()
    group.refresh_from_db()
    assert group.name == "Group2"

    # Delete
    group.delete()
    assert CustomGroup.objects.count() == 0
