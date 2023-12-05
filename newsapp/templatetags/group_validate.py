from django import template

# Create an instance of Library to register new template tags and filters
register = template.Library()


# Register a new filter using the decorator syntax
@register.filter
def user_in_group(user, group_name):
    """
    Custom template filter 'user_in_group'.

    This filter is designed to be used within Django templates to check if a given user belongs to a specified group.

    Args:
        user (User): The User object representing the current user.
        group_name (str): The name of the group to check for membership.

    Returns:
        bool: True if the user is a member of the specified group, False otherwise.

    Example Usage in Template:
        {% if request.user|user_in_group:'Editors' %}
            <!-- HTML to render if user is in the 'Editors' group -->
        {% endif %}

    This filter is useful for controlling the visibility of certain parts of a template based on the user's group membership.
    """

    # Checks if the given user is part of a group with the specified name and returns a boolean value.
    return user.groups.filter(name=group_name).exists()
