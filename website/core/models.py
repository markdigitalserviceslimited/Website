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


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().title()
        super().save(*args, **kwargs)


class BlogAuthor(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    role_or_title = models.CharField(
        max_length=150,
        default="Technical Contributor",
        help_text="e.g. 'Lead Systems Engineer', 'Managing Director', 'Growth Strategist'"
    )
    bio = models.TextField(
        blank=True,
        help_text="Short bio shown on article pages and author bylines"
    )
    avatar_image = models.ImageField(
        upload_to='blog/authors/',
        blank=True,
        null=True,
        help_text="Author profile photo"
    )
    avatar_initial = models.CharField(
        max_length=5,
        blank=True,
        default="",
        help_text="1-2 initials displayed when avatar image is not uploaded (auto-computed from name if left blank)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().title()
            if not self.avatar_initial or self.avatar_initial == "MD":
                parts = self.name.split()
                if parts:
                    self.avatar_initial = "".join(p[0].upper() for p in parts[:2])
                else:
                    self.avatar_initial = "MD"
        if not self.avatar_initial:
            self.avatar_initial = "MD"
        if self.role_or_title:
            self.role_or_title = self.role_or_title.strip().title()
        super().save(*args, **kwargs)


class AuthorSocialLink(models.Model):
    PLATFORM_CHOICES = (
        ('linkedin', 'LinkedIn'),
        ('twitter', 'X / Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('github', 'GitHub'),
        ('website', 'Personal / Portfolio Website'),
        ('email', 'Email Address'),
    )

    author = models.ForeignKey(
        BlogAuthor,
        on_delete=models.CASCADE,
        related_name='social_links'
    )
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    url = models.CharField(
        max_length=500,
        help_text="Full URL (e.g. 'https://linkedin.com/in/username') or email with 'mailto:'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Author Social Media Link"
        verbose_name_plural = "Author Social Media Links"

    def __str__(self):
        return f"{self.author.name} - {self.get_platform_display()}"

    def get_url(self):
        if not self.url:
            return "#"
        clean = self.url.strip()
        if self.platform == 'email':
            if not clean.startswith('mailto:') and '@' in clean:
                return f"mailto:{clean}"
            return clean
        if not clean.startswith(('http://', 'https://', 'mailto:')):
            return f"https://{clean}"
        return clean

    def save(self, *args, **kwargs):
        if self.url:
            self.url = self.url.strip()
            if self.platform == 'email':
                if not self.url.startswith('mailto:') and '@' in self.url:
                    self.url = f"mailto:{self.url}"
            else:
                if not self.url.startswith(('http://', 'https://')):
                    self.url = f"https://{self.url}"
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        BlogAuthor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        help_text="Select dynamic author from admin panel"
    )
    author_name = models.CharField(
        max_length=150,
        default="Mark Digital Team",
        help_text="Fallback author display name"
    )
    excerpt = models.TextField(
        help_text="Brief summary shown on blog preview cards and search results"
    )
    content = models.TextField(
        help_text="Main article content (HTML or plain text supported)"
    )
    read_time = models.CharField(
        max_length=50,
        default="5 min read",
        help_text="e.g. '4 min read'"
    )
    featured_image = models.ImageField(
        upload_to='blog/images/%Y/%m/',
        blank=True,
        null=True,
        help_text="Recommended size: 1200x675px (16:9 ratio)"
    )
    featured_image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text="Accessible description of the image"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    featured = models.BooleanField(
        default=False,
        help_text="Pin this article as the hero highlight on the blog page"
    )
    publish_date = models.DateTimeField(
        help_text="Publication date shown to visitors",
        null=True,
        blank=True
    )
    view_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO title (defaults to post title if blank)"
    )
    meta_description = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO description (defaults to excerpt if blank)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-publish_date', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or self.excerpt[:200]

    def get_author_display(self):
        if self.author:
            return self.author.name
        return self.author_name

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.strip().title()
        if self.author_name:
            self.author_name = self.author_name.strip().title()
        if self.author:
            self.author_name = self.author.name
        super().save(*args, **kwargs)



class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    client_title_or_role = models.CharField(
        max_length=150,
        help_text="e.g. 'Lead Consultant & Managing Director'"
    )
    organization = models.CharField(
        max_length=150,
        help_text="e.g. 'Abuja Advisory Partners'"
    )
    service_category = models.CharField(
        max_length=100,
        help_text="e.g. 'Web Platform & Digital Strategy'"
    )
    quote = models.TextField(
        help_text="Client feedback / review text"
    )
    avatar_initial = models.CharField(
        max_length=5,
        default="MD",
        help_text="1-2 initials displayed when avatar image is not uploaded (e.g. 'MB')"
    )
    avatar_image = models.ImageField(
        upload_to='testimonials/avatars/',
        blank=True,
        null=True,
        help_text="Optional client photo"
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        help_text="Star rating from 1 to 5"
    )
    verified = models.BooleanField(
        default=True,
        help_text="Show verified client badge"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display priority in the carousel (lower numbers first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide without deleting"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.client_name} ({self.organization})"

