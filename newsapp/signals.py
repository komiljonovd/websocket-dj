from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import News
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@receiver(post_save,sender=News)
def news_saved(sender,instance,created,**kwargs):
    channel_layer = get_channel_layer()

    if created:
        async_to_sync(channel_layer.group_send)(
            'news',
            {
                'type': 'new_news',
                'document': {
                    'id': instance.id,
                    'title': instance.title,
                    'short_description': instance.short_description,
                    'description': instance.description,
                    'created_at': instance.created_at.isoformat()
                }
            }
        )

        
    
    else:
        async_to_sync(channel_layer.group_send)(
            'news',
            {
                'type': 'update_news',
                'document': {
                    'id': instance.id,
                    'title': instance.title,
                    'short_description': instance.short_description,
                    'description': instance.description,
                    'created_at': instance.created_at.isoformat()
                }
            }
        )


@receiver(post_delete,sender=News)
def news_deleted(sender,instance,**kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'news',
        {
            'type': 'delete_news',
            'news_id': instance.id
        }
    )


