from django.db import models
# Create your models here.

class User(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.CharField(max_length=4095, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    USER_TYPE_CHOICES = (
        ('p', 'provider'),
        ('c', 'consumer'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='c')

    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('o', 'other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField()

    #CREATE A DEFAULT PROFILE PICTURE
    profile_picture = models.ImageField(blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Service_Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Service_Categories'

    def __str__(self):
        return self.name

class Service(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    provider = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Service_Category', on_delete=models.CASCADE, db_index=True)
    description = models.CharField(max_length=4095, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)

    def __str__(self):
        return self.title

class Service_Image(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField()

    class Meta:
        verbose_name_plural = 'Service_Images'

class Transaction(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    consumer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='consumer_transactions')
    provider = models.ForeignKey('User', on_delete=models.CASCADE, related_name='provider_transactions')
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    site_fee = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = (
        ('i', 'in_progress'),
        ('e', 'error'),
        ('c', 'completed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class Review(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author_reviews')
    provider = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True, related_name='provider_reviews')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, db_index=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()

class Message(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True, related_name='sender_messages')
	reciever = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True, related_name='reciever_messages')
	message_body = models.TextField()

class Dispute(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    disputer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='disputer_disputes')
    disputee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='disputee_disputes')
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    comment = models.TextField()

class Service_Price(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    tier_name = models.CharField(max_length=100, default="Base")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Service_Prices'

class Service_Time(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, db_index=True)
    time = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Service_Times'

class Booking(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	service = models.ForeignKey('Service', on_delete=models.CASCADE, db_index=True)
	consumer = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
	transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
	service_time = models.OneToOneField('Service_Time', on_delete=models.CASCADE, related_name='booking')
