from django.db import models


class CompanyInfo(models.Model):
    """Singleton-style company profile, editable from admin."""
    name = models.CharField(max_length=200, default='Tryvis Investments Limited')
    tagline = models.CharField(max_length=250, default='Precision engineering. Reliable supply. Built for industry.')
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, help_text='Upload the company logo here.')
    about = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    values = models.TextField()
    address_line = models.CharField(max_length=255, default='Plot 15, Msigani, Ubungo, Dar es Salaam')
    po_box = models.CharField(max_length=100, blank=True, default='P.O. Box 10952, Dar es Salaam')
    email = models.EmailField(default='tryvisinvestment@gmail.com')
    tin = models.CharField(max_length=50, blank=True, default='156-481-602')
    brela_reg_no = models.CharField(max_length=40, blank=True, help_text='BRELA Certificate of Incorporation number')
    business_license_no = models.CharField(max_length=60, blank=True, help_text='Business licence number, e.g. from the municipal council')
    whatsapp_number = models.CharField(max_length=30, blank=True, help_text='Digits with country code, e.g. 255767644317')

    class Meta:
        verbose_name = 'Company Info'
        verbose_name_plural = 'Company Info'

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=30)
    label = models.CharField(max_length=50, blank=True, help_text='e.g. Office, Sales, WhatsApp')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.number} ({self.label})' if self.label else self.number


class ServiceCategory(models.Model):
    """A line item Tryvis supplies or does — e.g. Bearings, Pneumatic Systems
    (a product line) or Engineering Workshop, Factory Audits (a service)."""
    KIND_CHOICES = [
        ('product', 'Product we supply'),
        ('service', 'Service we offer'),
    ]
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='service')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    icon_image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = 'Service categories'

    def __str__(self):
        return self.title


class Brand(models.Model):
    """A manufacturer brand Tryvis stocks (mainly bearings) — shown as a
    small trust strip on the Services page. Separate from Partner."""
    name = models.CharField(max_length=80)
    logo = models.ImageField(upload_to='brands/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('workshop', 'Workshop / Machine Works'),
        ('fabrication', 'Welding & Fabrication'),
        ('overhaul', 'Machine Overhauling'),
        ('gearbox', 'Gearbox Repair'),
        ('bearings', 'Bearings & Components'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f'Gallery image #{self.pk}'


class Partner(models.Model):
    """Client / partner logos shown in the trust strip."""
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class HeroSlide(models.Model):
    """Background images that cross-fade behind the homepage headline.

    Leave this table empty and the site falls back to three built-in
    engineering artworks, so the slider always looks finished.
    """
    image = models.ImageField(upload_to='hero/', help_text='Landscape photo, ideally 1920x1080 or wider.')
    headline = models.CharField(max_length=120, blank=True, help_text='Optional. Overrides the default headline while this slide is showing.')
    subline = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Hero slide'

    def __str__(self):
        return self.headline or f'Hero slide #{self.pk}'


class Stat(models.Model):
    """The short proof figures shown in the dark band on the homepage."""
    value = models.CharField(max_length=30, help_text='e.g. 2022, 7, 4')
    label = models.CharField(max_length=90, help_text='e.g. Serving industry since')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.value} — {self.label}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d %H:%M}'
