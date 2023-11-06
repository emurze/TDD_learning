from apps.list.models import ListItem


class ListItemMixin:
    def get_context_data(self, **kwargs) -> dict:
        kwargs['items'] = ListItem.objects.all()
        return super().get_context_data(**kwargs)
