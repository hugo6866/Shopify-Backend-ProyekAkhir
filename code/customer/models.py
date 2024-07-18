from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    STATE_CHOICES = [('disabled','disabled'),('invited','invited'),
                     ('enabled','enabled'), ('declined','declined')]
    user = models.ForeignKey(User,on_delete=models.RESTRICT, unique=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    verified_email = models.BooleanField(default=False)
    send_email_welcome = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='disabled')
    currency = models.CharField(max_length=10)
    @property
    def order_counts(self):
        return 0

    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    phone = models.CharField(max_length=100, null=True,blank=True)
    zip = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    default = models.BooleanField(default=False)
    @property
    def name(self):
        return self.customer.user.first_name + " " + self.customer.user.last_name
    
class Product(models.Model):
    STATUS_CHOICES = [('active','active'),('archived','archived'),
                     ('draft','draft')]
    title = models.CharField(max_length=255)
    body_html = models.TextField(blank=True)
    vendor = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handle = models.SlugField(max_length=255, unique=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    tags = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    inventory_quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight_unit = models.CharField(max_length=10, default='kg')
    
    requires_shipping = models.BooleanField(default=True)
    taxable = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class GiftCard(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    disabled_at = models.DateTimeField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)
    initial_value = models.DecimalField(max_digits=10, decimal_places=2)
    last_characters = models.CharField(max_length=4)
    line_item_id = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    template_suffix = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_characters = self.code[-4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
    
    
class Billing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('active', 'active'),
        ('declined', 'declined'),
        ('expired', 'expired'),
    ]

    confirmation_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    return_url = models.URLField(max_length=500)
    decoration_return_url = models.URLField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    test = models.BooleanField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"


class DiscountCodeCreationJob(models.Model):
    price_rule_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='queued')
    codes_count = models.IntegerField(default=0)
    imported_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    logs = models.JSONField(default=list)

class DiscountCode(models.Model):
    code = models.CharField(max_length=255)
    creation_job = models.ForeignKey(DiscountCodeCreationJob, on_delete=models.CASCADE, related_name='discount_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0)
    

class Order(models.Model):
    FINANCIAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('authorized', 'Authorized'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded'),
        ('voided', 'Voided'),
    ]

    FULFILLMENT_STATUS_CHOICES = [
        ('unfulfilled', 'Unfulfilled'),
        ('partial', 'Partially Fulfilled'),
        ('fulfilled', 'Fulfilled'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    financial_status = models.CharField(max_length=20, choices=FINANCIAL_STATUS_CHOICES, default='pending')
    fulfillment_status = models.CharField(max_length=20, choices=FULFILLMENT_STATUS_CHOICES, default='unfulfilled')

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_discounts = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    currency = models.CharField(max_length=3, default='USD')
    note = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True)

    discount_code = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    items = models.JSONField(default=list)

    cancel_reason = models.CharField(max_length=255, blank=True, null=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_number}"

    def add_item(self, product_id, quantity, price, variant_title=None):
        item = {
            'product_id': product_id,
            'quantity': quantity,
            'price': str(price),
            'variant_title': variant_title
        }
        self.items.append(item)
        self.save()

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.save()

    def get_items(self):
        return self.items
