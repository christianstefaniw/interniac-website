from django import template

"""
Custom template tags for the applications app  
Currently we support the following tag:

1. **filter_from_notif** - filter unread notifications by a certian listing
"""

register = template.Library()


@register.filter
def filter_from_notif(listing, user):
    """
    filters the current user's unread notifications by a certian listing  

    @type listing - `Listing`  
    @param listing - listing to show notifications for  
    @type user: `User``  
    @param user - the current user
    """
    notifs = user.notifications.unread()
    return notifs.filter(actor_object_id=listing.id)
