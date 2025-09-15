from api.models import Item

def get_all_items():
    return Item.objects.all()

def create_item(name=None, description=None, data=None):
    if data:
        name = data.get("name")
        description = data.get("description", "")
    return Item.objects.create(name=name, description=description)

def delete_item(item_id):
    return Item.objects.filter(id=item_id).delete()