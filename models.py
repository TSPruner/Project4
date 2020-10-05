from django.db import models

# Create your models here.
class Review(models.Model):
    RATINGS = (
        ('*', 'Really did not like'),
        ('**', 'Did not like'),
        ('***', 'Liked'),
        ('****', 'Loved'),
        ('*****', 'Really Loved'),
    )

    CHOICES = (
        (0, 'Tree'),
        (1, 'Wreath'),
        (2, 'Garland'),        
        (3, 'Centerpiece'),
        (4, 'MiniTree'),
        (5, 'TreeStand'),
        (6, 'Lights'),
        (7, 'TreeSkirt'),
        (8, 'Runner'),
        (9, 'Ribbon'),
        (10, 'Angel'),
        (11, 'Star'),
        (12, 'Bow'),
        (13, 'Bells'),
        (14, 'Bulbs'),
    )
    
    username = models.CharField(max_length=50)
    itemId = models.IntegerField()
    orderId = models.IntegerField(default=0)
    itemChoice = models.IntegerField(default=0, choices=CHOICES)
    rating = models.CharField(max_length=20, choices=RATINGS)
    comment = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"Review for ID #{self.itemId}, {dict(Review.CHOICES)[self.itemChoice]} order #{self.orderId} by {self.username}, {self.rating} and comment: {self.comment}"

class TreeStand(models.Model):
    TYPES = (
        ('Metal', 'Metal'),
        ('Plastic', 'Plastic'),
    )

    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    item = models.CharField(max_length=6, choices=TYPES)
    avail = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=5, choices=SIZE)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.item} Tree Stand for {self.price}"

class ChristmasGreen(models.Model):
    CHOICES = (
        (0, 'Balsam Fir'),
        (1, 'Fraser Fir'),
        (2, 'Canaan Fir'),
        (3, 'Douglas Fir'),
        (4, 'Grand Fir'),
        (5, 'Noble Fir'),
        (6, 'Concolor Fir'),
        (7, 'White Pine'),
        (8, 'Scotch Pine'),
        (9, 'Virginia Pine'),
        (10, 'Blue Spruce'),
        (11, 'Norway Spruce'),
        (12, 'White Spruce'),
        (13, 'Arizona Cypress'),
        (14, 'Leyland Cypress'),
        (15, 'Red Cedar'),
        (16, 'Holly'),
    )

    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    TYPES = (
        ('Tree', 'Tree'),
        ('Wreath', 'Wreath'),
        ('Garland', 'Garland'),
        ('Centerpiece', 'Centerpiece'),
        ('Minitree', 'Minitree'),
    )

    greenChoice = models.IntegerField(default=0, choices=CHOICES)
    item = models.CharField(max_length=15, choices=TYPES)
    smallAvail = models.BooleanField(default=True)
    largeAvail = models.BooleanField(default=True)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
   
    def __str__(self):
        phrase1 = "not available"

        if self.size == 'Small':
            if self.smallAvail:
                phrase1 = f"for ${self.price}"

        if self.size == 'Large':
            if self.largeAvail:
                phrase1 = f"for ${self.price}"

        return f"ID #{self.id} {self.size}, {dict(ChristmasGreen.CHOICES)[self.greenChoice]} {self.item} {phrase1}"

class Bow(models.Model):
    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Topper', 'Topper'),
    )

    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Blue', 'Blue'),
    )

    item = models.CharField(max_length=6, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)
    
    def __str__(self):
        if self.avail:
            phrase1 = f"for ${self.price}"
        else:
            phrase1 = "not available"

        if self.size == 'Topper':
            phrase2 = f"{self.size}, {self.item} Bow Tree Topper"
        else:
            phrase2 = f"{self.size}, {self.item} Bow Ornament"

        return f"ID #{self.id} {phrase2} {phrase1}"

class Bells(models.Model):
    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Topper', 'Topper'),
    )

    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Clear', 'Clear'),
    )

    item = models.CharField(max_length=7, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        if self.avail:
            phrase1 = f"for ${self.price}"
        else:
            phrase1 = "not available"

        if self.size == 'Topper':
            phrase2 = f"{self.size}, {self.item} Bells Tree Topper"
        else:
            phrase2 = f"{self.size}, {self.item} Bells Ornament"

        return f"ID #{self.id} {phrase2} {phrase1}"

class Star(models.Model):
    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Topper', 'Topper'),
    )

    TYPES = (
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Crystal', 'Crystal'),
    )

    item = models.CharField(max_length=7, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        if self.avail:
            phrase1 = f"for ${self.price}"
        else:
            phrase1 = "not available"

        if self.size == 'Topper':
            phrase2 = f"{self.size}, {self.item} Star Tree Topper"
        else:
            phrase2 = f"{self.size}, {self.item} Star Ornament"

        return f"ID #{self.id} {phrase2} {phrase1}"

class Angel(models.Model):
    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Topper', 'Topper'),
    )

    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Crystal', 'Crystal'),
        ('Blue', 'Blue'),
    )

    item = models.CharField(max_length=7, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        if self.avail:
            phrase1 = f"for ${self.price}"
        else:
            phrase1 = "not available"

        if self.size == 'Topper':
            phrase2 = f"{self.size}, {self.item} Angel Tree Topper"
        else:
            phrase2 = f"{self.size}, {self.item} Angel Ornament"

        return f"ID #{self.id} {phrase2} {phrase1}"

class Bulb(models.Model):
    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Crystal', 'Crystal'),
        ('Blue', 'Blue'),
    )

    item = models.CharField(max_length=7, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        return f"ID #{self.id} Box of {self.size}, {self.item} Bulbs for ${self.price}"

class Ribbon(models.Model):
    SIZE = (
        ('5 ft', '5 ft'),
        ('15 ft', '15 ft'),
        ('30 ft', '30 ft'),
    )

    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Blue', 'Blue'),
    )

    item = models.CharField(max_length=7, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.item} Ribbon for ${self.price}"

class Lights(models.Model):
    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Multi', 'Multi'),
        ('Blue', 'Blue'),
    )

    SIZE = (
        ('25 lights', '25 lights'),
        ('50 lights', '50 lights'),
        ('100 lights', '100 lights'),
        ('250 lights', '250 lights'),
        ('500 lights', '500 lights'),
    )

    item = models.CharField(max_length=5, choices=TYPES)
    size = models.CharField(max_length=10, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.item} Lights for ${self.price}"

class TableRunner(models.Model):
    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Trees', 'Trees'),
        ('Bells', 'Bells'),
        ('Wreaths', 'Wreaths'),
        ('Bows', 'Bows'),
        ('Candy Canes', 'Candy Canes'),
        ('Snowflakes', 'Snowflakes'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
    )

    SIZE = (
        ('4 ft', '4 ft'),
        ('8 ft', '8 ft'),
        ('12 ft', '12 ft'),
    )

    item = models.CharField(max_length=11, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.item} Table Runner for ${self.price}"

class TreeSkirt(models.Model):
    TYPES = (
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('White', 'White'),
        ('Trees', 'Trees'),
        ('Bells', 'Bells'),
        ('Wreaths', 'Wreaths'),
        ('Bows', 'Bows'),
        ('Candy Canes', 'Candy Canes'),
        ('Snowflakes', 'Snowflakes'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
    )

    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    item = models.CharField(max_length=11, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    avail = models.BooleanField(default=True)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.item} Tree Skirt for ${self.price}"


class Order(models.Model):
    STATE = (
        (0, 'Cancelled'),
        (1, 'Cart'),
        (2, 'Submitted'),
        (3, 'In Progress'),
        (4, 'Assembling'),
        (5, 'Shipped'),
        (6, 'Received'),
        (7, 'Completed'),
    )

    CHOICES = (
        (0, 'Tree'),
        (1, 'Wreath'),
        (2, 'Garland'),        
        (3, 'Centerpiece'),
        (4, 'MiniTree'),
        (5, 'TreeStand'),
        (6, 'Lights'),
        (7, 'TreeSkirt'),
        (8, 'Runner'),
        (9, 'Ribbon'),
        (10, 'Angel'),
        (11, 'Star'),
        (12, 'Bow'),
        (13, 'Bells'),
        (14, 'Bulbs'),
    )
    
    username = models.CharField(max_length=50)
    itemId = models.IntegerField()
    orderId = models.IntegerField(default=0)
    itemChoice = models.IntegerField(default=0, choices=CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.IntegerField(choices=STATE, default=1)
    itemDesc = models.CharField(default=None, max_length=100)
    specialInstructions = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return f"order# {self.orderId} for customer {self.username}: {self.itemDesc}"