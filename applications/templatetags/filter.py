from django import template

register = template.Library()


@register.filter
def filter_from_notif(listing, user):
    notifs = user.notifications.unread()
    return notifs.filter(actor_object_id=listing.id)
