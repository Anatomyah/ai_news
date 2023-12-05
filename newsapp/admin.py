from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

# Unregisters the default Group model from Django admin.
# This step is necessary to replace the default Group admin interface.
admin.site.unregister(Group)


class GroupAdminWithPermissions(GroupAdmin):
    """
    Custom admin class 'GroupAdminWithPermissions'.

    This class extends Django's default GroupAdmin to modify the admin interface for Group model.
    Specifically, it changes the way permissions are displayed and managed in the Django admin panel.

    Attributes:
        filter_horizontal (list): Specifies the fields that should use a horizontal filter interface.
                                  In this case, it is set for 'permissions' to improve usability.

    By using this custom admin class, the display and management of group permissions become more user-friendly,
    especially when dealing with a large number of permissions.

    Example Usage:
    This class is registered with Django's admin site to replace the default Group admin interface.
    """

    # Sets the permissions field to use a horizontal filter interface, enhancing the user interface for admin.
    filter_horizontal = ['permissions']


# Registers the Group model with the customized GroupAdminWithPermissions.
# This replaces the default admin interface for Group with the enhanced version.
admin.site.register(Group, GroupAdminWithPermissions)
