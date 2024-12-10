from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Cart


@receiver(m2m_changed, sender=Cart.dishes.through)
def update_cart_totals(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.calculate_subtotal()
        instance.calculate_total()
        instance.save()
