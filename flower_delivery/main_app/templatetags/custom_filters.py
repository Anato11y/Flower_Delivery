from django import template

register = template.Library()

@register.filter
def chunk(items, chunk_size):
    """
    Разбивает список на группы по chunk_size элементов.
    """
    try:
        chunk_size = int(chunk_size)
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    except (ValueError, TypeError):
        return [items]

