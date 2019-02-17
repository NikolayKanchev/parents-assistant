from django import template

from home.models import Category, SizeFilter, SharedSizeFilter

register = template.Library()


@register.filter
def get_categories(section):
    return section.category_set.filter(section=section).order_by("pk")


@register.filter
def get_photos(child):
    return child.photo_set.filter(child=child).order_by("pk")


@register.filter
def get_num_items(category):
    size_filter = SizeFilter.objects.filter(child=category.section.child).first()

    if category.section.name == "Clothes":
        count = 0
        clothing_sizes = size_filter.clothing_size
        category_items = category.item_set.filter(category=category)

        if clothing_sizes:
            for item in category_items:
                if item.clothing_size[0] in clothing_sizes:
                    count += 1
            return count
        else:
            return category_items.count()

    if category.section.name == "Shoes":
        count = 0
        shoe_sizes = size_filter.shoe_size
        category_items = category.item_set.filter(category=category)

        if shoe_sizes:
            for item in category_items:
                if item.shoe_size[0] in shoe_sizes:
                    count += 1
            return count
        else:
            return category_items.count()

    else:
        return category.item_set.filter(category=category).count()


@register.simple_tag
def get_shared_child_num_items(category, user_pk):
    size_filter = SharedSizeFilter.objects.filter(child=category.section.child).first()

    if category.section.name == "Clothes":
        count = 0
        clothing_sizes = size_filter.clothing_size
        category_items = category.item_set.filter(category=category)

        if clothing_sizes:
            for item in category_items:
                if item.clothing_size[0] in clothing_sizes:
                    count += 1
            return count
        else:
            return category_items.count()

    if category.section.name == "Shoes":
        count = 0
        shoe_sizes = size_filter.shoe_size
        category_items = category.item_set.filter(category=category)

        if shoe_sizes:
            for item in category_items:
                if item.shoe_size[0] in shoe_sizes:
                    count += 1
            return count
        else:
            return category_items.count()

    else:
        return category.item_set.filter(category=category).count()
