from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from accounts.models import User
from home.forms import ChildForm, PreemieForm, NotBornChildForm, UpdateSizeSystemForm, UpdateSizesForm, \
    UpdateShoeSizesForm, SectionForm, CategoryForm, UpdateCategoryForm, UpdateSectionForm, ItemForm, \
    UpdateClothingSizeFilterForm, UpdateShoeSizeFilterForm, UpdateItemForm, UpdateSharedClothingSizeFilterForm, \
    UpdateSharedShoeSizeFilterForm
from home.models import Child, Section, Category, Item, SizeFilter, SharedSizeFilter
from .models import Photo
from .forms import PhotoForm


# class JSONResponseMixin:
#     """
#     A mixin that can be used to render a JSON response.
#     """
#     def render_to_json_response(self, context, **response_kwargs):
#         """
#         Returns a JSON response, transforming 'context' to make the payload.
#         """
#         return JsonResponse(
#             self.get_data(context),
#             **response_kwargs
#         )
#
#     def get_data(self, context):
#         """
#         Returns an object that will be serialized as JSON by json.dumps().
#         """
#         # Note: This is *EXTREMELY* naive; in reality, you'll need
#         # to do much more complex handling to ensure that arbitrary
#         # objects -- such as Django model instances or querysets
#         # -- can be serialized as JSON.
#         return context


class HomeView(ListView):
    template_name = 'home/index.html'
    context_object_name = 'children'

    def get_queryset(self):
        return Child.objects.filter(user=self.request.user.pk).order_by("pk")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView,
                        self).get_context_data(object_list=None, **kwargs)

        context['default_categories'] = Category.get_default_category_names()

        if 'pk' in self.kwargs:

            obj = Child.objects.filter(pk=self.kwargs['pk']).first()
            context['chosen_child'] = obj

            sections = Section.objects.filter(child=obj).order_by('pk')
            context['chosen_child_sections'] = sections

            photo = Photo.objects.filter(child=obj).first()
            context['chosen_child_photo'] = photo

            size_filter = SizeFilter.objects.filter(child=obj).first()
            context['size_filter'] = size_filter

            if obj is not None and obj.age is None:
                context['not_born_yet'] = True
            else:
                context['not_born_yet'] = False

        else:

            obj = Child.objects.filter(user=self.request.user.pk).last()
            context['chosen_child'] = obj

            sections = Section.objects.filter(child=obj).order_by('pk')
            context['chosen_child_sections'] = sections

            photo = Photo.objects.filter(child=obj).first()
            context['chosen_child_photo'] = photo

            size_filter = SizeFilter.objects.filter(child=obj).first()
            context['size_filter'] = size_filter

            if obj is not None and obj.age is None:
                context['not_born_yet'] = True
            else:
                context['not_born_yet'] = False

        return context


class SharedHomeView(HomeView):

    def get_queryset(self):
        return Child.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView,
                        self).get_context_data(object_list=None, **kwargs)

        if 'slug' in self.kwargs:
            context['slug'] = self.kwargs['slug']

        context['default_categories'] = Category.get_default_category_names()

        context['shared_child'] = "shared_child"
        context['logged_user'] = self.request.user.pk

        obj = Child.objects.filter(pk=self.kwargs['pk']).first()
        context['chosen_child'] = obj

        sections = Section.objects.filter(child=obj).order_by('pk')
        context['chosen_child_sections'] = sections

        photo = Photo.objects.filter(child=obj).first()
        context['chosen_child_photo'] = photo

        size_filter = SharedSizeFilter.objects.filter(child=obj, user=self.request.user.pk).first()
        context['size_filter'] = size_filter

        if obj is not None and obj.age is None:
            context['not_born_yet'] = True
        else:
            context['not_born_yet'] = False

        return context


class AddFullTermChildView(CreateView):
    model = Child
    template_name = 'home/add_full_term_child.html'
    form_class = ChildForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(AddFullTermChildView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AddPreemieView(CreateView):
    model = Child
    template_name = 'home/add_preemie.html'
    form_class = PreemieForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(AddPreemieView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AddNotBornView(CreateView):
    model = Child
    template_name = 'home/add_not_born_child.html'
    form_class = NotBornChildForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(AddNotBornView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateChildView(UpdateView):
    model = Child
    template_name = 'home/update_child.html'
    form_class = ChildForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateChildView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# class UpdateShareView(UpdateView):
#     model = Child
#     template_name = 'home/update_share.html'
#     form_class = ChildShareForm
#
#     def get_success_url(self):
#         return reverse('home', args=(self.object.id,))
#
#     def get_form_kwargs(self):
#         kwargs = super(UpdateShareView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs


class ShareChildView(TemplateView):
    template_name = 'home/update_share.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShareChildView,
                        self).get_context_data(object_list=None, **kwargs)

        if 'pk' in self.kwargs:

            child = Child.objects.filter(pk=self.kwargs['pk']).first()
            context['chosen_child'] = child
            context['shared_with'] = child.shared_with.values()
            context['shared_with_edit'] = child.shared_with_edit.values()

        return context


class SharedWithMe(TemplateView):
    template_name = 'home/shared_with_me.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SharedWithMe,
                        self).get_context_data(object_list=None, **kwargs)

        context['shared_with'] = Child.objects.filter(shared_with=self.request.user.pk)
        context['shared_with_edit'] = Child.objects.filter(shared_with_edit=self.request.user.pk)

        return context


def share_child_with(request):
    data = request.GET
    email = data.get('email')
    child_pk = data.get('child_pk')
    editOrRead = data.get('editOrRead')

    child = Child.objects.get(pk=child_pk)
    user = User.objects.filter(email=email).first()

    if user:
        if user == request.user:
            data_to_return = {
                'error': "You can not share with your self"
            }
            return JsonResponse(data_to_return)

        if user in child.shared_with.all():
            data_to_return = {
                'error': "You already share the child's info with this user !"
            }
        elif user in child.shared_with_edit.all():
            data_to_return = {
                'error': "You already share the child's info with this user !"
            }
        else:

            if user in child.shared_with_edit.all():
                data_to_return = {
                    'error': "User with this e-mail address doesn't exist in the system !"
                }

            if editOrRead == "read":
                child.shared_with.add(user)
                child.save()
                sf = SizeFilter.objects.get(child=child)
                SharedSizeFilter.objects.create(child=child, user=user, clothing_size=sf.clothing_size,
                                                shoe_size=sf.shoe_size)
                data_to_return = {
                    'success': f"The child's info was successfully shared with {user.first_name}",
                    'user_name': f"{user.first_name} {user.last_name}",
                    "user_pk": user.pk,
                }
            else:
                child.shared_with_edit.add(user)
                child.save()
                sf = SizeFilter.objects.get(child=child)
                SharedSizeFilter.objects.create(child=child, user=user, clothing_size=sf.clothing_size,
                                                shoe_size=sf.shoe_size)
                data_to_return = {
                    'success': f"The child's info was successfully shared with {user.first_name}",
                    'user_name': f"{user.first_name} {user.last_name}",
                    "user_pk": user.pk,
                }
    else:
        data_to_return = {
            'error': "User with this e-mail address doesn't exist in the system !"
        }

    return JsonResponse(data_to_return)


def change_share_privileges(request):
    data = request.GET
    user_pk = data.get('user_pk')
    child_pk = data.get('child_pk')

    child = Child.objects.get(pk=child_pk)
    user = User.objects.get(pk=user_pk)

    if data.get('delete'):
        if user in child.shared_with.all():
            child.shared_with.remove(user)
        else:
            child.shared_with_edit.remove(user)

        SharedSizeFilter.objects.get(child=child, user=user).delete()

        data_to_return = {
            'success': "The user doesn't have privileges any more !"
        }
        return JsonResponse(data_to_return)

    if user in child.shared_with.all():
        child.shared_with.remove(user)
        child.shared_with_edit.add(user)
        data_to_return = {
            'success': "The user privileges were updated successfully !"
        }
    elif user in child.shared_with_edit.all():
        child.shared_with_edit.remove(user)
        child.shared_with.add(user)
        data_to_return = {
            'success': "The user privileges were updated successfully !"
        }
    else:
        data_to_return = {
            'error': "Something went wrong !"
        }

    return JsonResponse(data_to_return)


class DeleteChildView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Child
    success_url = reverse_lazy('home')

    def test_func(self):
        """ Only let the user access this page if they own the object being deleted"""
        return self.get_object().user == self.request.user


class UpdateSizeSystemView(UpdateView):
    model = Child
    template_name = 'home/update_size_system.html'
    form_class = UpdateSizeSystemForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateSizeSystemView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateSizesView(UpdateView):
    model = Child
    template_name = 'home/update_sizes.html'
    form_class = UpdateSizesForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateSizesView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateShoeSizesView(UpdateView):
    model = Child
    template_name = 'home/update_shoe_sizes.html'
    form_class = UpdateShoeSizesForm

    def get_success_url(self):
        return reverse('home', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateShoeSizesView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AddSectionView(CreateView):
    model = Section
    template_name = 'home/add_section.html'
    form_class = SectionForm

    def get_success_url(self):
        return reverse('home', args=(self.object.child.id,))

    def get_form_kwargs(self):
        kwargs = super(AddSectionView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class AddCategoryView(CreateView):
    model = Category
    template_name = 'home/add_category.html'
    form_class = CategoryForm

    def get_success_url(self):
        section = Section.objects.filter(pk=self.kwargs.get('pk')).first()
        return reverse('home', args=(section.child.pk,))

    def get_form_kwargs(self):
        kwargs = super(AddCategoryView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class UpdateCategoryView(UpdateView):
    model = Category
    template_name = 'home/update_category.html'
    form_class = UpdateCategoryForm

    def get_success_url(self):
        return reverse('home', args=(self.object.section.child.pk,))

    def get_form_kwargs(self):
        kwargs = super(UpdateCategoryView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class UpdateSectionView(UpdateView):
    model = Section
    template_name = 'home/update_section.html'
    form_class = UpdateSectionForm

    def get_success_url(self):
        return reverse('home', args=(self.object.child.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateSectionView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class DeleteCategoryView(DeleteView):
    model = Category

    def get_success_url(self):
        return reverse('home', args=(self.object.section.child.pk,))


class DeleteSectionView(DeleteView):
    model = Section

    def get_success_url(self):
        return reverse('home', args=(self.object.child.id,))


# class MainSectionView(JSONResponseMixin, TemplateView):
#
#     def post(self, request, *args, **kwargs):
#         id = request.POST.get('id')
#
#         data = {'rating': question.rating}
#
#         return self.render_to_response(data)
#
#     def render_to_response(self, context, **response_kwargs):
#         return self.render_to_json_response(context, **response_kwargs)

class AddItemsView(CreateView):
    model = Item
    template_name = 'home/add_update_items.html'
    form_class = ItemForm

    def get_success_url(self):
        if self.request.user in self.object.category.section.child.shared_with.all():
            return reverse('shared-home-view', args=(self.object.category.section.child.id, 'read'))
        elif self.request.user in self.object.category.section.child.shared_with_edit.all():
            return reverse('shared-home-view', args=(self.object.category.section.child.id, 'edit'))
        else:
            return reverse('home', args=(self.object.category.section.child.id,))

    def get_form_kwargs(self):
        kwargs = super(AddItemsView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        kwargs.update({'child': Category.objects.filter(pk=self.kwargs.get('pk')).first().section.child})
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddItemsView,
                        self).get_context_data(object_list=None, **kwargs)
        if 'pk' in self.kwargs:
            obj = Category.objects.filter(pk=self.kwargs['pk']).first()
            context['category_name'] = obj.name
            context['section_name'] = obj.section.name
        return context


class ItemsView(TemplateView):
    template_name = 'home/items_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemsView,
                        self).get_context_data(object_list=None, **kwargs)

        if 'slug' in self.kwargs:
            context['slug'] = self.kwargs['slug']

        context['children'] = Child.objects.filter(user=self.request.user.pk)

        if 'pk' in self.kwargs:
            category = Category.objects.filter(pk=self.kwargs['pk']).first()
            context['category'] = category
            child = category.section.child
            context['chosen_child'] = child

            if 'slug' not in self.kwargs:
                size_filter = SizeFilter.objects.filter(child=child).first()
            else:
                size_filter = SharedSizeFilter.objects.filter(child=child).first()

            context['size_filter'] = size_filter

            items = Item.objects.filter(category=self.kwargs['pk']).order_by("pk")

            filtered_items = []
            for item in items:
                if item.clothing_size:
                    if item.clothing_size[0] in size_filter.clothing_size:
                        filtered_items.append(item)

                elif item.shoe_size:
                    if item.shoe_size[0] in size_filter.shoe_size:
                        filtered_items.append(item)

                else:
                    filtered_items = items

            context['items'] = filtered_items

        return context


class AllItemsView(ListView):
    template_name = 'home/all_items_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(category=self.kwargs['pk']).order_by("pk")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllItemsView,
                        self).get_context_data(object_list=None, **kwargs)

        if 'pk' in self.kwargs:
            category = Category.objects.filter(pk=self.kwargs['pk']).first()
            size_filter = SizeFilter.objects.filter(child=category.section.child).first()
            context['size_filter'] = size_filter
            context['category'] = category

        return context


class UpdateItemView(UpdateView):
    model = Item
    template_name = 'home/add_update_items.html'
    form_class = UpdateItemForm

    def get_success_url(self):
        # if 'slug' in self.kwargs:
        #     return reverse('all_items_list', args=(self.object.category.id,))
        # else:
        return reverse('items_list', args=(self.object.category.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateItemView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        kwargs.update({'item': Item.objects.filter(pk=self.kwargs.get('pk')).first()})
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpdateItemView,
                        self).get_context_data(object_list=None, **kwargs)
        if 'pk' in self.kwargs:
            obj = Item.objects.filter(pk=self.kwargs.get('pk')).first()
            # context['c_name'] = obj.category.name
            context['section_name'] = obj.category.section.name
        if 'slug' in self.kwargs:
            context['slug'] = self.kwargs.get('slug')
        return context


class DeleteItemView(DeleteView):
    model = Item

    def get_success_url(self):
        if 'slug' in self.kwargs:
            return reverse('all_items_list', args=(self.object.category.id,))
        else:
            return reverse('items_list', args=(self.object.category.id,))


class PhotoView(UpdateView):
    model = Photo
    template_name = 'home/update_photo.html'
    form_class = PhotoForm

    def get_success_url(self):
        return reverse('crop-photo', args=(self.object.pk, ))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhotoView,
                        self).get_context_data(object_list=None, **kwargs)

        photo = Photo.objects.filter(pk=self.kwargs['pk']).first()
        context['child_photo'] = photo

        return context


class UpdateClothingFilterSizesView(UpdateView):
    model = SizeFilter
    template_name = 'home/update_clothing_sizes_filter.html'
    form_class = UpdateClothingSizeFilterForm

    def get_success_url(self):
        if len(self.kwargs) > 1:
            return reverse('items_list', args=(self.kwargs['category_pk'],))
        else:
            return reverse('home', args=(self.object.child.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateClothingFilterSizesView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class UpdateSharedClothingFilterSizesView(UpdateView):
    model = SharedSizeFilter
    template_name = 'home/update_clothing_sizes_filter.html'
    form_class = UpdateSharedClothingSizeFilterForm

    def get_success_url(self):
        privileges = ''
        if self.request.user in self.object.child.shared_with.all():
            privileges = 'read'
        elif self.request.user in self.object.child.shared_with_edit.all():
            privileges = 'edit'

        if len(self.kwargs) > 1:
            return reverse('items_list', args=(self.kwargs['category_pk'], privileges))
        else:
            return reverse('shared-home-view', args=(self.object.child.id, privileges))

    def get_form_kwargs(self):
        kwargs = super(UpdateSharedClothingFilterSizesView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class UpdateShoeFilterSizesView(UpdateView):
    model = SizeFilter
    template_name = 'home/update_shoe_sizes_filter.html'
    form_class = UpdateShoeSizeFilterForm

    def get_success_url(self):
        if len(self.kwargs) > 1:
            return reverse('items_list', args=(self.kwargs['category_pk'],))
        else:
            return reverse('home', args=(self.object.child.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateShoeFilterSizesView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


class UpdateSharedShoeFilterSizesView(UpdateView):
    model = SharedSizeFilter
    template_name = 'home/update_shoe_sizes_filter.html'
    form_class = UpdateSharedShoeSizeFilterForm

    def get_success_url(self):
        privileges = ''
        if self.request.user in self.object.child.shared_with.all():
            privileges = 'read'
        elif self.request.user in self.object.child.shared_with_edit.all():
            privileges = 'edit'

        if len(self.kwargs) > 1:
            return reverse('items_list', args=(self.kwargs['category_pk'], privileges))
        else:
            return reverse('shared-home-view', args=(self.object.child.id, privileges))

    def get_form_kwargs(self):
        kwargs = super(UpdateSharedShoeFilterSizesView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs.get('pk')})
        return kwargs


def delete_items(request):
    data = request.GET
    items_to_delete = data.get('items')
    items_to_delete = items_to_delete.split(',')

    for item_pk in items_to_delete:
        item = Item.objects.filter(pk=item_pk).first()
        if item:
            item.delete()

    data_to_return = {
        'success': "The items were deleted successfully !!!",
    }

    return JsonResponse(data_to_return)


def move_items(request):
    data = request.GET
    items_to_delete = data.get('items')
    items_to_delete = items_to_delete.split(',')

    for item_pk in items_to_delete:
        item = Item.objects.filter(pk=item_pk).first()
        if item:
            item.delete()

    data_to_return = {
        'success': "The items were deleted successfully !!!",
    }

    return JsonResponse(data_to_return)


def move_items_to_another_child(request):
    data = request.GET
    items_ids = data.get('items')
    toChild = Child.objects.get(pk=data.get('toChild'))
    items_to_move = items_ids.split(',')

    first_item = Item.objects.filter(pk=items_to_move[0]).first()
    from_section = first_item.category.section
    from_category = first_item.category
    sections_another_child = Section.objects.filter(child=toChild)

    data_to_return = {}
    count = 0
    for section in sections_another_child:
        if from_section.name == section.name:
            count += 1
            data_to_return = move_items_to_child(from_category, section, items_to_move)

    if count == 0:
        section = Section.objects.create(child=toChild, name=from_section.name)
        data_to_return = move_items_to_child(from_category, section, items_to_move)

    return JsonResponse(data_to_return)


def move_items_to_child(from_category, section, items_to_move):

    count = 0
    for category in section.category_set.values():
        if from_category.name == category['name']:
            count += 1
            for item_pk in items_to_move:
                item = Item.objects.filter(pk=item_pk).first()
                if item:
                    item.category = Category.objects.get(pk=category['id'])
                    item.save()

    if count:
        return {"success": "The items were moved successfully"}
    else:
        category = Category.objects.create(section=section, name=from_category.name)

        count += 1
        for item_pk in items_to_move:
            item = Item.objects.filter(pk=item_pk).first()
            if item:
                item.category = category
                item.save()
        return {"success": "The items were moved successfully"}

# class UpdateClothingFilterSizesSecondView(UpdateClothingFilterSizesView):
#     def get_success_url(self):
#         category_pk = self.kwargs['category_pk']
#         return reverse('items_list', args=(category_pk,))
#
#
# class UpdateShoeFilterSizesSecondView(UpdateShoeFilterSizesView):
#     def get_success_url(self):
#         category_pk = self.kwargs['category_pk']
#         return reverse('items_list', args=(category_pk,))