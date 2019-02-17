from django.forms import HiddenInput, TextInput

from accounts.models import User
from home.models import Child, Section, Category, Item, SizeFilter, SharedSizeFilter

from PIL import Image
from django import forms
from .models import Photo


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        exclude = ('shared_with_me', 'shared_with_me_can_edit',)

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user')
        super(ChildForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True

        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['date_of_birth'].widget = TextInput(attrs={'class': 'dp'})
        self.fields['size_system'].widget = HiddenInput()
        self.initial['child_status'] = Child.F
        self.fields['child_status'].widget = HiddenInput()
        self.fields['due_date'].widget = HiddenInput()


class PreemieForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PreemieForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True
        self.fields['due_date'].required = True

        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['date_of_birth'].widget = TextInput(attrs={'class': 'dp'})
        self.fields['size_system'].widget = HiddenInput()
        self.initial['child_status'] = Child.P
        self.fields['child_status'].widget = HiddenInput()
        self.fields['due_date'].widget = TextInput(attrs={'class': 'dp_due_date'})


class NotBornChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NotBornChildForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].required = True

        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['size_system'].widget = HiddenInput()
        self.initial['name'] = "Coming Soon"
        self.fields['name'].widget = HiddenInput()
        self.initial['child_status'] = Child.N
        self.fields['child_status'].widget = HiddenInput()
        self.fields['due_date'].widget = TextInput(attrs={'class': 'dp_due_date'})


class UpdateSizeSystemForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['user', 'name', 'size_system']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateSizeSystemForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['name'].widget = HiddenInput()


# class ChildShareForm(forms.ModelForm):
#     class Meta:
#         model = Child
#         fields = ['user', 'shared_with_me', 'shared_with_me_can_edit']
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super(ChildShareForm, self).__init__(*args, **kwargs)
#         self.fields['user'].queryset = User.objects.filter(pk=user.pk)
#         self.initial['user'] = User.objects.filter(pk=user.pk).first()
#         self.fields['user'].widget = HiddenInput()
#         self.fields['shared_with_me'].queryset = User.objects.exclude(pk=user.pk)
#         self.fields['shared_with_me_can_edit'].queryset = User.objects.exclude(pk=user.pk)


class UpdateSizesForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['user', 'name', 'size_system', 'corrected_sizes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateSizesForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['name'].widget = HiddenInput()
        self.fields['size_system'].widget = HiddenInput()
        self.fields['corrected_sizes'].choices = kwargs['instance'].sizes


class UpdateShoeSizesForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['user', 'name', 'size_system', 'corrected_shoe_sizes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateShoeSizesForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.pk)
        self.initial['user'] = User.objects.filter(pk=user.pk).first()
        self.fields['user'].widget = HiddenInput()
        self.fields['name'].widget = HiddenInput()
        self.fields['size_system'].widget = HiddenInput()
        self.fields['corrected_shoe_sizes'].choices = kwargs['instance'].shoe_sizes


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['child'].queryset = Child.objects.all()
        self.initial['child'] = Child.objects.filter(pk=self.pk).first()
        self.fields['child'].widget = HiddenInput()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.all()
        self.initial['section'] = Section.objects.filter(pk=self.pk).first()
        self.fields['section'].widget = HiddenInput()


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(UpdateCategoryForm, self).__init__(*args, **kwargs)
        self.fields['section'].widget = HiddenInput()


class UpdateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(UpdateSectionForm, self).__init__(*args, **kwargs)
        self.fields['child'].widget = HiddenInput()


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.child = kwargs.pop('child')
        super(ItemForm, self).__init__(*args, **kwargs)
        category = Category.objects.filter(pk=self.pk).first()
        self.fields['category'].queryset = Category.objects.filter(pk=self.pk)
        self.initial['category'] = category
        self.fields['category'].widget = HiddenInput()

        if category.section.name == "Clothes":
            self.fields['clothing_size'].required = True
            self.fields['clothing_size'].choices = self.child.sizes

        if category.section.name == "Shoes":
            self.fields['shoe_size'].required = True
            self.fields['shoe_size'].choices = self.child.shoe_sizes


class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.item = kwargs.pop('item')
        super(UpdateItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(section=self.item.category.section)
        self.initial['category'] = self.item.category
        self.fields['category'].widget = HiddenInput()
        self.fields['amount'].widget = HiddenInput()

        if self.item.category.section.name == "Clothes":
            self.fields['clothing_size'].required = True
            self.fields['clothing_size'].choices = self.item.category.section.child.sizes

        if self.item.category.section.name == "Shoes":
            self.fields['shoe_size'].required = True
            self.fields['shoe_size'].choices = self.item.category.section.child.shoe_sizes


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', 'child')
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['child'].widget = HiddenInput()

    def save(self, **kwargs):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class UpdateClothingSizeFilterForm(forms.ModelForm):
    class Meta:
        model = SizeFilter
        fields = ['child', 'clothing_size']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        super(UpdateClothingSizeFilterForm, self).__init__(*args, **kwargs)
        self.fields['child'].widget = HiddenInput()

        self.fields['clothing_size'].required = True
        self.fields['clothing_size'].choices = self.instance.child.sizes


class UpdateSharedClothingSizeFilterForm(forms.ModelForm):
    class Meta:
        model = SharedSizeFilter
        fields = ['child', 'clothing_size']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        super(UpdateSharedClothingSizeFilterForm, self).__init__(*args, **kwargs)
        self.fields['child'].widget = HiddenInput()

        self.fields['clothing_size'].required = True
        self.fields['clothing_size'].choices = self.instance.child.sizes


class UpdateShoeSizeFilterForm(forms.ModelForm):
    class Meta:
        model = SizeFilter
        fields = ['child', 'shoe_size']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        super(UpdateShoeSizeFilterForm, self).__init__(*args, **kwargs)

        self.fields['child'].widget = HiddenInput()

        self.fields['shoe_size'].required = True
        self.fields['shoe_size'].choices = self.instance.child.shoe_sizes


class UpdateSharedShoeSizeFilterForm(forms.ModelForm):
    class Meta:
        model = SharedSizeFilter
        fields = ['child', 'shoe_size']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        super(UpdateSharedShoeSizeFilterForm, self).__init__(*args, **kwargs)

        self.fields['child'].widget = HiddenInput()

        self.fields['shoe_size'].required = True
        self.fields['shoe_size'].choices = self.instance.child.shoe_sizes
