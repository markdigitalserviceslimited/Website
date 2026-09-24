from django.db import models


class QuoteRequest(models.Model):
    SERVICE_CHOICES = [
        ('web_development', 'Website Design & Software Development'),
        ('social_media', 'Social Media Management'),
        ('digital_marketing', 'Business Promotion & Digital Marketing'),
        ('digital_branding', 'Digital Branding & Creative Content'),
        ('tech_training', 'Technology Training & Skill Development'),
        ('ict_supply', 'ICT Equipment & Tech Accessories Supply'),
        ('multiple', 'Multiple / Integrated Digital Services'),
    ]

    BUDGET_CHOICES = [
        ('undecided', 'Not yet decided / Flexible'),
        ('tier_1', '₦250,000 – ₦500,000'),
        ('tier_2', '₦500,000 – ₦1,500,000'),
        ('tier_3', '₦1,500,000 – ₦3,500,000'),
        ('tier_4', '₦3,500,000+ (Enterprise Scope)'),
    ]

    TIMELINE_CHOICES = [
        ('immediate', 'Immediately (Within 1-2 weeks)'),
        ('normal', 'Standard (2-4 weeks)'),
        ('quarter', 'Upcoming Quarter / 1-3 months'),
        ('exploring', 'Just exploring possibilities'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Enquiry'),
        ('in_review', 'In Review'),
        ('contacted', 'Client Contacted'),
        ('closed', 'Closed / Converted'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    business_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Business or Organization Name")
    email = models.EmailField(verbose_name="Email Address")
    phone_or_whatsapp = models.CharField(max_length=50, verbose_name="Phone or WhatsApp Number")
    service_needed = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='web_development', verbose_name="Service Needed")
    project_description = models.TextField(verbose_name="Project Scope & Objectives")
    estimated_budget = models.CharField(max_length=50, choices=BUDGET_CHOICES, default='tier_1', verbose_name="Estimated Budget")
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, default='normal', verbose_name="Expected Timeline")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"

    def __str__(self):
        return f"{self.full_name} ({self.business_name or 'Individual'}) - {self.get_service_needed_display()}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    target_audience = models.CharField(max_length=255, help_text="e.g. SMEs, Startups, NGOs, Creators")
    key_benefit = models.CharField(max_length=255)
    capabilities_list = models.TextField(help_text="Newline-separated list of capabilities")
    icon_svg = models.TextField(blank=True, help_text="Inline SVG code for custom icon")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_capabilities(self):
        return [cap.strip() for cap in self.capabilities_list.split('\n') if cap.strip()]


class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=200)
    category = models.CharField(max_length=150)
    milestone_stat = models.CharField(max_length=100, help_text="e.g. 200,000+ YouTube Subscribers")
    objective = models.TextField()
    outcome = models.TextField()
    support_areas = models.TextField(help_text="Newline-separated support areas delivered")
    testimonial_quote = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"

    def __str__(self):
        return f"{self.client_name} - {self.title}"

    def get_support_areas(self):
        return [area.strip() for area in self.support_areas.split('\n') if area.strip()]


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
