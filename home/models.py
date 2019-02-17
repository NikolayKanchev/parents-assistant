from dateutil.relativedelta import *
from datetime import date
from django.db import models
from django.db.models import CASCADE
from multiselectfield import MultiSelectField

from accounts.models import User


class Child(models.Model):

    # region ****************************** STATIC **************************************
    SIZES_DICT = {
        '32': 0, '38': 1, '44': 2, '50': 3, '56': 4, '62': 5, '68': 6, '74': 7, '80': 8, '86': 9, '92': 10, '98': 11,
        '104': 12, '110': 13, '116': 14, '122': 15, '128': 16, '134': 17, '140': 18, '146': 19, '152': 20,
        '-': 0, '--': 1, '---': 2, '----': 3, '0m': 4, '3m': 5, '6m': 6, '9m': 7, '12m': 8, '18m': 9, '24m': 10, '2': 11,
        '3': 12, '4': 13, '5': 14, '6': 15, '7': 16, '8': 17, '9': 18, '10': 19, '11': 20, '12': 21,
        'new3': 3, '2T': 11, '3T': 12, '4T': 13, '6X-7': 16, '14': 21,
    }

    SHOE_SIZES_DICT = {
        '15': 0, '16': 1, '17': 2, '18': 3, '19': 4, '20': 5, '21': 6, '22': 7, '23': 8, '24': 9, '25': 10, '26': 11,
        '26.5': 12, '27': 13, '28': 14, '29': 15, '30': 16, '31': 17, '32': 18, '33': 19, '34': 20, '35': 21, '36': 22,
        '37': 23, '38': 24,

        '0': 0, '0.5': 1, '1.5': 2, '2.5': 3, '3': 4, '3.5': 5, '4.5': 6, '5.5': 7, '6': 8, '7': 9, '7.5': 10, '8.5': 11,
        '9': 12, '9.5': 13, '10': 14, '11': 15, '11.5': 16, '12.5': 17, '13': 18, '1 ': 19, '2 ': 20, '2.5 ': 21,
        '3.5 ': 22, '4 ': 23, '5 ': 24,

        ' 0': 0, ' 1': 1, ' 2': 2, ' 3': 3, ' 4': 4, ' 4.5': 5, ' 5.5': 6, ' 6.5': 7, ' 7': 8, ' 8': 9, ' 8.5': 10,
        ' 9.5': 11, ' 10': 12, ' 10.5': 13, ' 11': 14, ' 12': 15, ' 12.5': 16, ' 13.5': 17, ' 1 ': 18, ' 2 ': 19,
        ' 3 ': 20, ' 3.5 ': 21, ' 4.5 ': 22, ' 5 ': 23, ' 6 ': 24,

    }

    CLOTHING_SIZES = {
        'EU': ((0, '32'), (1, '38'), (2, '44'), (3, '50'), (4, '56'), (5, '62'), (6, '68'), (7, '74'), (8, '80'),
               (9, '86'), (10, '92'), (11, '98'), (12, '104'), (13, '110'), (14, '116'), (15, '122'), (16, '128'),
               (17, '134'), (18, '140'), (19, '146'), (20, '152'), (21, '152')),

        'UK': ((0, '-'), (1, '--'), (2, '---'), (3, '----'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2'), (12, '3'), (13, '4'), (14, '5'), (15, '6'), (16, '7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '12')),

        'US': ((0, '-'), (1, '--'), (2, '---'), (3, 'new3'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2T'), (12, '3T'), (13, '4T'), (14, '5'), (15, '6'), (16, '6X-7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '14')),
    }

    SHOE_SIZES = {
        'EU': ((0, '15'), (1, '16'), (2, '17'), (3, '18'), (4, '19'), (5, '20'), (6, '21'), (7, '22'), (8, '23'),
               (9, '24'), (10, '25'), (11, '26'), (12, '26.5'), (13, '27'), (14, '28'), (15, '29'), (16, '30'),
               (17, '31'), (18, '32'), (19, '33'), (20, '34'), (21, '35'), (22, '36'), (23, '37'),
               (24, '38')),
        'UK': ((0, '0'), (1, '0.5'), (2, '1.5'), (3, '2.5'), (4, '3'), (5, '3.5'), (6, '4.5'), (7, '5.5'), (8, '6'),
               (9, '7'), (10, '7.5'), (11, '8.5'), (12, '9'), (13, '9.5'), (14, '10'), (15, '11'), (16, '11.5'),
               (17, '12.5'), (18, '13'), (19, '1 '), (20, '2 '), (21, '2.5 '), (22, '3.5 '), (23, '4 '),
               (24, '5 ')),
        'US': ((0, ' 0'), (1, ' 1'), (2, ' 2'), (3, ' 3'), (4, ' 4'), (5, ' 4.5'), (6, ' 5.5'), (7, ' 6.5'), (8, ' 7'),
               (9, ' 8'), (10, ' 8.5'), (11, ' 9.5'), (12, ' 10'), (13, ' 10.5'), (14, ' 11'), (15, ' 12'), (16, ' 12.5'),
               (17, ' 13.5'), (18, ' 1 '), (19, ' 2 '), (20, ' 3 '), (21, ' 3.5 '), (22, ' 4.5 '), (23, ' 5 '),
               (24, ' 6 ')),
    }

    F, P, N = "F", "P", "Not born yet"
    CHILD_STATUS_CHOICES = (
        (F, "Full term"),
        (P, "Preemie"),
        (N, 'Not born yet'),
    )

    CHILD_GENDER_CHOICES = (
        ("BOY", 'Boy'),
        ("GIRL", 'Girl'),
    )

    EU, UK, US = 'EU', "UK", "US"
    SIZE_SYSTEMS = (
        (EU, "EU"),
        (UK, "UK"),
        (US, "US"),
    )

    # endregion

    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=5, choices=CHILD_GENDER_CHOICES, default=None, blank=True, null=True)
    # picture = models.ImageField(upload_to='', default='pic_folder/None/no-img.jpg', blank=True)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    size_system = models.CharField(max_length=5, choices=SIZE_SYSTEMS, default="EU")
    child_status = models.CharField(max_length=15, choices=CHILD_STATUS_CHOICES, default="F")
    due_date = models.DateField(default=None, blank=True, null=True)
    clothes_size_difference = models.IntegerField(default=None, blank=True, null=True)
    shoe_size_difference = models.IntegerField(default=None, blank=True, null=True)

    corrected_sizes = MultiSelectField(choices=CLOTHING_SIZES.get("EU"), max_choices=2, default=None, blank=True, null=True)
    corrected_shoe_sizes = MultiSelectField(choices=SHOE_SIZES.get("EU"), max_choices=2, default=None, blank=True, null=True)

    shared_with = models.ManyToManyField(User, related_name="shared_with_me", default=None, blank=True)
    shared_with_edit = models.ManyToManyField(User, related_name="shared_with_me_can_edit", default=None, blank=True)

    @property
    def age(self):
        today = date.today()
        if self.date_of_birth is not None:
            age = relativedelta(today, date(self.date_of_birth.year, self.date_of_birth.month, self.date_of_birth.day))
            return age
        else:
            return

    # region *********************************** CLOTHES ******************************************
    """The possible clothes sizes"""
    @property
    def sizes(self):
        return self.CLOTHING_SIZES.get(self.size_system)

    @property
    def get_clothes_size(self):

        if self.age.years == 0 and self.age.months == 0:
            return self.sizes[3][1], self.sizes[4][1]

        if self.age.years == 0 and 3 > self.age.months >= 1:
            return self.get_size_for_period(0, 3, self.sizes[4][1], self.sizes[5][1])

        if self.age.years == 0 and 6 > self.age.months >= 3:
            return self.get_size_for_period(3, 6, self.sizes[5][1], self.sizes[6][1])

        if self.age.years == 0 and 9 > self.age.months >= 6:
            return self.get_size_for_period(6, 9, self.sizes[6][1], self.sizes[7][1])

        if self.age.years == 0 and 12 > self.age.months >= 9:
            return self.get_size_for_period(9, 12, self.sizes[7][1], self.sizes[8][1])

        if self.age.years == 1 and 6 > self.age.months >= 0:
            return self.get_size_for_period(0, 6, self.sizes[8][1], self.sizes[9][1])

        if self.age.years == 1 and 12 > self.age.months >= 6:
            return self.get_size_for_period(6, 12, self.sizes[9][1], self.sizes[10][1])

        if self.age.years == 2 and 12 > self.age.months >= 0:
            return self.get_size_for_period(0, 12, self.sizes[10][1], self.sizes[11][1])

        if 4 >= self.age.years >= 3:
            return self.get_size_for_period(0, 0, self.sizes[11][1], self.sizes[12][1], 3, 4)

        if 5 >= self.age.years >= 4:
            return self.get_size_for_period(0, 0, self.sizes[12][1], self.sizes[13][1], 4, 5)

        if 6 >= self.age.years >= 5:
            return self.get_size_for_period(0, 0, self.sizes[13][1], self.sizes[14][1], 5, 6)

        if 7 >= self.age.years >= 6:
            return self.get_size_for_period(0, 0, self.sizes[14][1], self.sizes[15][1], 6, 7)

        if 8 >= self.age.years >= 7:
            return self.get_size_for_period(0, 0, self.sizes[15][1], self.sizes[16][1], 7, 8)

        if 9 >= self.age.years >= 8:
            return self.get_size_for_period(0, 0, self.sizes[16][1], self.sizes[17][1], 8, 9)

        if 10 >= self.age.years >= 9:
            return self.get_size_for_period(0, 0, self.sizes[17][1], self.sizes[18][1], 9, 10)

        if 11 >= self.age.years >= 10:
            return self.get_size_for_period(0, 0, self.sizes[18][1], self.sizes[19][1], 10, 11)

        if 12 >= self.age.years >= 11:
            return self.get_size_for_period(0, 0, self.sizes[19][1], self.sizes[20][1], 11, 12)

    # Just the string representation
    def get_clothes_sizes_str(self):

        if self.get_clothes_size:
            if type(self.get_clothes_size) is tuple:
                size_difference = self.get_clothes_size_difference(self.get_clothes_size[1])
                if size_difference is None:
                    size_difference = 0
                size1_index = self.SIZES_DICT.get(self.get_clothes_size[0]) + size_difference
                size1 = self.sizes[size1_index]
                size2_index = self.SIZES_DICT.get(self.get_clothes_size[1]) + size_difference
                size2 = self.sizes[size2_index]

                return f"{size1[1]} - {size2[1]}"
            else:
                size_difference = self.get_clothes_size_difference(self.get_clothes_size)
                if size_difference is None:
                    size_difference = 0
                size1_index = self.SIZES_DICT.get(self.get_clothes_size) + size_difference
                size1 = self.sizes[size1_index]

                return f"{size1[1]}"

    def get_clothes_size_difference(self, estimated_size):

        if self.corrected_sizes is not None:
            if len(self.corrected_sizes) == 0:
                self.corrected_sizes = None
                self.save()
                return self.clothes_size_difference
            elif len(self.corrected_sizes) == 1:
                self.clothes_size_difference = int(self.corrected_sizes[0]) - self.SIZES_DICT.get(estimated_size)
                self.corrected_sizes = None
                self.save()
                return self.clothes_size_difference
            elif len(self.corrected_sizes) == 2:
                self.clothes_size_difference = int(self.corrected_sizes[1]) - self.SIZES_DICT.get(estimated_size)
                self.corrected_sizes = None
                self.save()
                return self.clothes_size_difference
            # elif len(self.corrected_sizes) == 3:
            #     self.clothes_size_difference = int(self.corrected_sizes[2]) - self.SIZES_DICT.get(estimated_size)
            #     self.corrected_sizes = None
            #     self.save()
            #     return self.clothes_size_difference
        else:
            if self.clothes_size_difference is None:
                return 0
            else:
                return self.clothes_size_difference

    # It is used many times in the get_clothes_size() and get_shoe_size() property.
    # It returns the right size based on the which part of the period (the beginning, the end or the middle)
    def get_size_for_period(self, first_month, last_month, first_size, second_size, first_year=0, second_year=0):
        if first_year and second_year:
            if self.age.years == first_year and 0 <= self.age.months <= 6:
                return first_size
            if self.age.years == first_year and 6 < self.age.months <= 12:
                return first_size, second_size
            if self.age.years == second_year and 0 <= self.age.months <= 6:
                return first_size, second_size
            if self.age.years == second_year and 6 < self.age.months <= 12:
                return second_size
        else:
            if first_month <= self.age.months <= (first_month + ((last_month - first_month) / 3 - 1)):
                return first_size
            if (last_month - ((last_month - first_month) / 3 - 1)) <= self.age.months <= last_month:
                return second_size
            if (first_month + (last_month - first_month) / 3 - 1) < \
                    self.age.months < (last_month - ((last_month - first_month) / 3 - 1)):
                return first_size, second_size
# endregion

    # region ************************************ SHOES *******************************************
    """The possible shoe sizes"""
    @property
    def shoe_sizes(self):
        return self.SHOE_SIZES.get(self.size_system)

    @property
    def get_shoe_size(self):

        if self.age.years == 0 and self.age.months == 0:
            return self.shoe_sizes[0][1]

        if self.age.years == 0 and 3 > self.age.months >= 1:
            return self.get_size_for_period(0, 3, self.shoe_sizes[0][1], self.shoe_sizes[1][1])

        if self.age.years == 0 and 6 > self.age.months >= 3:
            return self.shoe_sizes[2][1]

        if self.age.years == 0 and 9 > self.age.months >= 6:
            return self.shoe_sizes[3][1]

        if self.age.years == 0 and 12 > self.age.months >= 9:
            return self.shoe_sizes[4][1]

        if self.age.years == 1 and 3 > self.age.months >= 0:
            return self.shoe_sizes[5][1]

        if self.age.years == 1 and 5 > self.age.months >= 3:
            return self.shoe_sizes[6][1]

        if self.age.years == 1 and 8 > self.age.months >= 5:
            return self.shoe_sizes[7][1]

        if self.age.years == 1 and 12 > self.age.months >= 8:
            return self.shoe_sizes[8][1]

        if 3 >= self.age.years >= 2:
            return self.get_size_for_period(0, 0, self.shoe_sizes[9][1], self.shoe_sizes[10][1], 2, 3)

        if 4 >= self.age.years >= 3:
            return self.get_size_for_period(0, 0, self.shoe_sizes[11][1], self.shoe_sizes[12][1], 3, 4)

        if 5 >= self.age.years >= 4:
            return self.get_size_for_period(0, 0, self.shoe_sizes[12][1], self.shoe_sizes[13][1], 4, 5)

        if self.age.years == 5:
            return self.shoe_sizes[14][1]

        if self.age.years == 6:
            return self.shoe_sizes[15][1]

        if self.age.years == 7:
            return self.shoe_sizes[16][1]

        if self.age.years == 8:
            return self.shoe_sizes[17][1]

        if self.age.years == 9:
            return self.shoe_sizes[18][1]

        if self.age.years == 10:
            return self.shoe_sizes[19][1]

        if self.age.years == 11:
            return self.shoe_sizes[20][1]

        if self.age.years == 12:
            return self.shoe_sizes[21][1]

        if self.age.years == 13:
            return self.shoe_sizes[22][1]

        if self.age.years == 14:
            return self.shoe_sizes[23][1]

        if self.age.years == 15:
            return self.shoe_sizes[24][1]

    # Just the string representation
    def get_shoe_sizes_str(self):
        if self.get_shoe_size:
            if type(self.get_shoe_size) is tuple:
                size_difference = self.get_shoe_size_difference(self.get_shoe_size[1])
                size1_index = self.SHOE_SIZES_DICT.get(self.get_shoe_size[0]) + size_difference
                size1 = self.shoe_sizes[size1_index]
                size2_index = self.SHOE_SIZES_DICT.get(self.get_shoe_size[1]) + size_difference
                size2 = self.shoe_sizes[size2_index]

                return f"{size1[1]} - {size2[1]}"
            else:
                size_difference = self.get_shoe_size_difference(self.get_shoe_size)
                size1_index = self.SHOE_SIZES_DICT.get(self.get_shoe_size) + size_difference
                size1 = self.shoe_sizes[size1_index]

                return f"{size1[1]}"

    def get_shoe_size_difference(self, estimated_size):
        if self.corrected_shoe_sizes is not None:
            if len(self.corrected_shoe_sizes) == 0:
                self.corrected_shoe_sizes = None
                self.save()
                if self.shoe_size_difference is None:
                    self.shoe_size_difference = 0
                return self.shoe_size_difference
            elif len(self.corrected_shoe_sizes) == 1:
                self.shoe_size_difference = int(self.corrected_shoe_sizes[0]) - self.SHOE_SIZES_DICT.get(estimated_size)
                self.corrected_shoe_sizes = None
                self.save()
                return self.shoe_size_difference
            elif len(self.corrected_shoe_sizes) == 2:
                self.shoe_size_difference = int(self.corrected_shoe_sizes[1]) - self.SHOE_SIZES_DICT.get(estimated_size)
                self.corrected_shoe_sizes = None
                self.save()
                return self.shoe_size_difference
            # elif len(self.corrected_shoe_sizes) == 3:
            #     self.shoe_size_difference = int(self.corrected_shoe_sizes[2]) - self.SHOE_SIZES_DICT.get(estimated_size)
            #     self.corrected_shoe_sizes = None
            #     self.save()
            #     return self.shoe_size_difference
        else:
            if self.shoe_size_difference is None:
                return 0
            else:
                return self.shoe_size_difference

    # endregion


class Section(models.Model):
    child = models.ForeignKey(Child, on_delete=CASCADE)
    name = models.CharField(max_length=50)

    @staticmethod
    def get_default_sections_names():
        return 'Clothes', 'Shoes', 'Toys'


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=CASCADE, default=None)
    name = models.CharField(max_length=50, default=None, blank=True)

    @property
    def num_items(self):
        return Item.objects.filter(category=self.pk).count()

    @staticmethod
    def get_default_category_names():
        return ('Snowsuits & jackets', 'Knitwear & sweatshirts', 'Blouses & shirts',
                'T-shirts', 'Bodysuits with long sleeves', 'Bodysuits with short sleeves',
                'Sleepsuits', 'Dresses & skirts', 'Trousers', 'Leggings', 'Jeans', 'Shorts',
                'Pyjamas', 'Tights', 'Underwear', 'Accessories', 'Swimwear',
                'Boots', 'Sneakers', 'Sandals', 'Toys', 'Baby', 'Outdoor', 'Musical')


class Item(models.Model):
    CLOTHING_SIZES = {
        'EU': ((0, '32'), (1, '38'), (2, '44'), (3, '50'), (4, '56'), (5, '62'), (6, '68'), (7, '74'), (8, '80'),
               (9, '86'), (10, '92'), (11, '98'), (12, '104'), (13, '110'), (14, '116'), (15, '122'), (16, '128'),
               (17, '134'), (18, '140'), (19, '146'), (20, '152'), (21, '152')),

        'UK': ((0, '-'), (1, '--'), (2, '---'), (3, '----'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2'), (12, '3'), (13, '4'), (14, '5'), (15, '6'), (16, '7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '12')),

        'US': ((0, '-'), (1, '--'), (2, '---'), (3, 'new3'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2T'), (12, '3T'), (13, '4T'), (14, '5'), (15, '6'), (16, '6X-7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '14')),
    }

    SHOE_SIZES = {
        'EU': ((0, '15'), (1, '16'), (2, '17'), (3, '18'), (4, '19'), (5, '20'), (6, '21'), (7, '22'), (8, '23'),
               (9, '24'), (10, '25'), (11, '26'), (12, '26.5'), (13, '27'), (14, '28'), (15, '29'), (16, '30'),
               (17, '31'), (18, '32'), (19, '33'), (20, '34'), (21, '35'), (22, '36'), (23, '37'),
               (24, '38')),
        'UK': ((0, '0'), (1, '0.5'), (2, '1.5'), (3, '2.5'), (4, '3'), (5, '3.5'), (6, '4.5'), (7, '5.5'), (8, '6'),
               (9, '7'), (10, '7.5'), (11, '8.5'), (12, '9'), (13, '9.5'), (14, '10'), (15, '11'), (16, '11.5'),
               (17, '12.5'), (18, '13'), (19, '1 '), (20, '2 '), (21, '2.5 '), (22, '3.5 '), (23, '4 '),
               (24, '5 ')),
        'US': ((0, ' 0'), (1, ' 1'), (2, ' 2'), (3, ' 3'), (4, ' 4'), (5, ' 4.5'), (6, ' 5.5'), (7, ' 6.5'), (8, ' 7'),
               (9, ' 8'), (10, ' 8.5'), (11, ' 9.5'), (12, ' 10'), (13, ' 10.5'), (14, ' 11'), (15, ' 12'),
               (16, ' 12.5'),
               (17, ' 13.5'), (18, ' 1 '), (19, ' 2 '), (20, ' 3 '), (21, ' 3.5 '), (22, ' 4.5 '), (23, ' 5 '),
               (24, ' 6 ')),
    }

    N, AN, UF = 'New', 'As good as new', 'Used but fine'
    CONDITION_CHOICES = (
        (N, 'New'),
        (AN, 'As good as new'),
        (UF, 'Used but fine'),
    )

    B, G, U = 'Boy', 'Girl', 'Unisex'
    SEX_CHOICES = (
        (B, 'Boy'),
        (G, 'Girl'),
        (U, 'Unisex'),
    )

    W, SP, SU, A = 'Winter', 'Spring', 'Summer', 'Autumn'
    SEASON_CHOICES = (
        (W, 'Winter'),
        (SP, 'Spring'),
        (SU, 'Summer'),
        (A, 'Autumn'),
    )

    BLACK, WHITE, RED, BLUE, PURPLE, GREEN, YELLOW, ORANGE, BROWN, GREY = \
        'Black', 'White', 'Red', 'Blue', 'Purple', 'Green', 'Yellow', 'Orange', 'Brown', 'Grey',
    COLOR_CHOICES = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (PURPLE, 'Purple'),
        (GREEN, 'Green'),
        (YELLOW, 'Yellow'),
        (ORANGE, 'Orange'),
        (BROWN, 'Brown'),
        (GREY, 'Grey'),
    )

    category = models.ForeignKey(Category, on_delete=CASCADE)
    picture = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg', blank=True)
    note = models.TextField(max_length=500, default=None, blank=True, null=True)
    brand = models.CharField(max_length=50, default=None, blank=True, null=True)
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default="New")
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default=None, blank=True, null=True)
    season = models.CharField(max_length=7, choices=SEASON_CHOICES, default=None, blank=True, null=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default=None, blank=True, null=True)
    price = models.FloatField(default=None, blank=True, null=True)
    amount = models.IntegerField(default=1, blank=True, null=True)

    clothing_size = MultiSelectField(choices=CLOTHING_SIZES.get("EU"), max_choices=1, default=None, blank=True, null=True)
    shoe_size = MultiSelectField(choices=SHOE_SIZES.get("EU"), max_choices=1, default=None, blank=True, null=True)

    @property
    def get_clothing_size(self):
        sizes = self.category.section.child.sizes
        return sizes[int(self.clothing_size[0])][1]

    @property
    def get_shoe_size(self):
        sizes = self.category.section.child.shoe_sizes
        return sizes[int(self.shoe_size[0])][1]


class Photo(models.Model):
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    child = models.ForeignKey(Child, on_delete=CASCADE, default=None)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


class SizeFilter(models.Model):

    CLOTHING_SIZES = {
        'EU': ((0, '32'), (1, '38'), (2, '44'), (3, '50'), (4, '56'), (5, '62'), (6, '68'), (7, '74'), (8, '80'),
               (9, '86'), (10, '92'), (11, '98'), (12, '104'), (13, '110'), (14, '116'), (15, '122'), (16, '128'),
               (17, '134'), (18, '140'), (19, '146'), (20, '152'), (21, '152')),

        'UK': ((0, '-'), (1, '--'), (2, '---'), (3, '----'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2'), (12, '3'), (13, '4'), (14, '5'), (15, '6'), (16, '7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '12')),

        'US': ((0, '-'), (1, '--'), (2, '---'), (3, 'new3'), (4, '0m'), (5, '3m'), (6, '6m'), (7, '9m'), (8, '12m'),
               (9, '18m'), (10, '24m'), (11, '2T'), (12, '3T'), (13, '4T'), (14, '5'), (15, '6'), (16, '6X-7'),
               (17, '8'), (18, '9'), (19, '10'), (20, '11'), (21, '14')),
    }

    SHOE_SIZES = {
        'EU': ((0, '15'), (1, '16'), (2, '17'), (3, '18'), (4, '19'), (5, '20'), (6, '21'), (7, '22'), (8, '23'),
               (9, '24'), (10, '25'), (11, '26'), (12, '26.5'), (13, '27'), (14, '28'), (15, '29'), (16, '30'),
               (17, '31'), (18, '32'), (19, '33'), (20, '34'), (21, '35'), (22, '36'), (23, '37'),
               (24, '38')),
        'UK': ((0, '0'), (1, '0.5'), (2, '1.5'), (3, '2.5'), (4, '3'), (5, '3.5'), (6, '4.5'), (7, '5.5'), (8, '6'),
               (9, '7'), (10, '7.5'), (11, '8.5'), (12, '9'), (13, '9.5'), (14, '10'), (15, '11'), (16, '11.5'),
               (17, '12.5'), (18, '13'), (19, '1 '), (20, '2 '), (21, '2.5 '), (22, '3.5 '), (23, '4 '),
               (24, '5 ')),
        'US': ((0, ' 0'), (1, ' 1'), (2, ' 2'), (3, ' 3'), (4, ' 4'), (5, ' 4.5'), (6, ' 5.5'), (7, ' 6.5'), (8, ' 7'),
               (9, ' 8'), (10, ' 8.5'), (11, ' 9.5'), (12, ' 10'), (13, ' 10.5'), (14, ' 11'), (15, ' 12'),
               (16, ' 12.5'),
               (17, ' 13.5'), (18, ' 1 '), (19, ' 2 '), (20, ' 3 '), (21, ' 3.5 '), (22, ' 4.5 '), (23, ' 5 '),
               (24, ' 6 ')),
    }

    child = models.ForeignKey(Child, on_delete=CASCADE)

    clothing_size = MultiSelectField(choices=CLOTHING_SIZES.get("EU"), default=None, blank=True,
                                     null=True)
    shoe_size = MultiSelectField(choices=SHOE_SIZES.get("EU"), default=None, blank=True, null=True)

    @property
    def get_clothing_sizes(self):
        sizes = self.child.sizes
        sizes_to_return = ""
        for size in self.clothing_size:
            if sizes_to_return == "":
                sizes_to_return += (sizes[int(size)][1])
            else:
                sizes_to_return += ", " + (sizes[int(size)][1])

        return sizes_to_return

    @property
    def get_shoe_sizes(self):
        sizes = self.child.shoe_sizes
        sizes_to_return = ""
        for size in self.shoe_size:
            if sizes_to_return == "":
                sizes_to_return += (sizes[int(size)][1])
            else:
                sizes_to_return += ", " + (sizes[int(size)][1])

        return sizes_to_return


class SharedSizeFilter(SizeFilter):
    user = models.ForeignKey(User, on_delete=CASCADE, default=None)


class StorageBag(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)

