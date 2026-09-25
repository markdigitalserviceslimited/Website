from django.db import migrations
from django.utils import timezone


def get_or_create_category(BlogCategory, slug, name, description):
    cat = BlogCategory.objects.filter(slug=slug).first() or BlogCategory.objects.filter(name__iexact=name).first()
    if cat:
        cat.slug = slug
        cat.name = name
        cat.description = description
        cat.save()
        return cat
    return BlogCategory.objects.create(slug=slug, name=name, description=description)


def get_or_create_author(BlogAuthor, slug, name, role_or_title, bio, avatar_initial, is_active=True):
    author = BlogAuthor.objects.filter(slug=slug).first() or BlogAuthor.objects.filter(name__iexact=name).first()
    if author:
        author.slug = slug
        author.name = name
        author.role_or_title = role_or_title
        author.bio = bio
        author.avatar_initial = avatar_initial
        author.is_active = is_active
        author.save()
        return author
    return BlogAuthor.objects.create(
        slug=slug,
        name=name,
        role_or_title=role_or_title,
        bio=bio,
        avatar_initial=avatar_initial,
        is_active=is_active
    )


def seed_data(apps, schema_editor):
    BlogCategory = apps.get_model('core', 'BlogCategory')
    BlogAuthor = apps.get_model('core', 'BlogAuthor')
    AuthorSocialLink = apps.get_model('core', 'AuthorSocialLink')
    BlogPost = apps.get_model('core', 'BlogPost')
    Testimonial = apps.get_model('core', 'Testimonial')

    # 1. Categories
    cat_web = get_or_create_category(
        BlogCategory,
        slug='web-engineering-tech',
        name='Web Engineering & Tech',
        description='Modern web development, performance architecture, and full-stack software.'
    )
    cat_growth = get_or_create_category(
        BlogCategory,
        slug='digital-growth-marketing',
        name='Digital Growth & Marketing',
        description='Audience growth, SEO, YouTube monetization, and conversion optimization.'
    )
    cat_ict = get_or_create_category(
        BlogCategory,
        slug='ict-hardware-infrastructure',
        name='ICT & Hardware Infrastructure',
        description='Enterprise ICT hardware procurement, office networking, and tech equipment.'
    )
    cat_skills = get_or_create_category(
        BlogCategory,
        slug='tech-skills-mentorship',
        name='Tech Skills & Mentorship',
        description='Workforce upskilling, practical tech bootcamps, and career growth.'
    )
    cat_demo = get_or_create_category(
        BlogCategory,
        slug='demo',
        name='Demo',
        description='Demo category.'
    )

    # 2. Authors
    a_akor = get_or_create_author(
        BlogAuthor,
        slug='akor-mark-akoji',
        name='Akor Mark Akoji',
        role_or_title='Managing Director & Lead Consultant',
        bio='Managing Director of Mark Digital Services LTD, specializing in web architecture, enterprise technology solutions, digital strategy, and business growth advisory.',
        avatar_initial='AM'
    )
    AuthorSocialLink.objects.get_or_create(author=a_akor, platform='linkedin', defaults={'url': 'https://www.linkedin.com/in/akor-mark-akoji', 'order': 1})
    AuthorSocialLink.objects.get_or_create(author=a_akor, platform='facebook', defaults={'url': 'https://www.facebook.com/', 'order': 2})
    AuthorSocialLink.objects.get_or_create(author=a_akor, platform='email', defaults={'url': 'mailto:markdigitalserviceslimited@gmail.com', 'order': 3})

    a_deepak = get_or_create_author(
        BlogAuthor,
        slug='deepak-kumar-das',
        name='Deepak Kumar Das',
        role_or_title='Software Engineer',
        bio='Full-stack software engineer at Mark Digital Services LTD specializing in scalable web systems and modern frontend architectures.',
        avatar_initial='DK'
    )
    AuthorSocialLink.objects.get_or_create(author=a_deepak, platform='facebook', defaults={'url': 'https://www.facebook.com', 'order': 1})
    AuthorSocialLink.objects.get_or_create(author=a_deepak, platform='github', defaults={'url': 'https://www.github.com/callmedas', 'order': 2})
    AuthorSocialLink.objects.get_or_create(author=a_deepak, platform='email', defaults={'url': 'mailto:deepakkdas77@gmail.com', 'order': 3})

    a_desk = get_or_create_author(
        BlogAuthor,
        slug='mark-digital-engineering-desk',
        name='Mark Digital Engineering Desk',
        role_or_title='Systems & Infrastructure Engineering',
        bio='The technical engineering division at Mark Digital Services LTD, covering full-stack web software, cloud infrastructure, and verified ICT hardware deployment.',
        avatar_initial='MD'
    )
    AuthorSocialLink.objects.get_or_create(author=a_desk, platform='website', defaults={'url': 'https://markdigital.com.ng', 'order': 1})
    AuthorSocialLink.objects.get_or_create(author=a_desk, platform='github', defaults={'url': 'https://github.com/', 'order': 2})
    AuthorSocialLink.objects.get_or_create(author=a_desk, platform='email', defaults={'url': 'mailto:markdigitalserviceslimited@gmail.com', 'order': 3})

    a_growth = get_or_create_author(
        BlogAuthor,
        slug='mark-digital-growth-team',
        name='Mark Digital Growth Team',
        role_or_title='Digital Growth & Media Strategy',
        bio='Specialists in audience development, YouTube monetization algorithms, ROI-driven marketing funnels, and creative digital branding.',
        avatar_initial='MG'
    )
    AuthorSocialLink.objects.get_or_create(author=a_growth, platform='youtube', defaults={'url': 'https://www.youtube.com/', 'order': 1})
    AuthorSocialLink.objects.get_or_create(author=a_growth, platform='facebook', defaults={'url': 'https://www.facebook.com/', 'order': 2})
    AuthorSocialLink.objects.get_or_create(author=a_growth, platform='email', defaults={'url': 'mailto:markdigitalserviceslimited@gmail.com', 'order': 3})

    # 3. Testimonials
    Testimonial.objects.get_or_create(
        client_name='Mr. Ben',
        defaults={
            'client_title_or_role': 'YouTube Creator & Media Partner',
            'organization': '200,000+ Subscriber Channel',
            'service_category': 'YouTube Monetization & Growth',
            'quote': 'Mark Digital Services LTD provided practical support that helped us improve our YouTube presence, audience growth and approach to monetization. Seeing the channel grow beyond 200,000 subscribers has been a major milestone.',
            'avatar_initial': 'MB',
            'rating': 5,
            'verified': True,
            'order': 1,
            'is_active': True,
        }
    )

    # 4. Blog Posts
    now = timezone.now()
    p1 = BlogPost.objects.filter(slug='how-modern-web-architecture-accelerates-business-revenue').first()
    if not p1:
        BlogPost.objects.create(
            slug='how-modern-web-architecture-accelerates-business-revenue',
            title='How Modern Web Architecture Accelerates Business Revenue In 2026',
            category=cat_web,
            author=a_akor,
            author_name='Akor Mark Akoji',
            excerpt='Why responsive engineering, blazing page speeds, and clean software architecture are direct revenue drivers for Nigerian businesses and growing African enterprises.',
            content='<p>In today\'s fast-moving digital economy, a website is no longer just an online brochure—it is your business\'s 24/7 sales engine, customer service hub, and brand flagship.</p><h2>1. Speed Directly Dictates Conversion Rates</h2><p>Research across global digital commerce shows that every additional second of page load time reduces conversion rates by up to 7%. For companies targeting users on mobile networks across Nigeria and West Africa, lightweight, optimized code is an absolute competitive advantage.</p><h2>2. Trust Signals and Corporate Credibility</h2><p>Prospective corporate clients, investors, and high-value buyers research your digital presence before ever reaching out. A glitchy layout, broken mobile menu, or slow interface immediately erodes credibility. Conversely, an intuitive, beautifully styled portal establishes authoritative competence from the first interaction.</p>',
            read_time='5 min read',
            status='published',
            featured=True,
            publish_date=now,
        )

    p2 = BlogPost.objects.filter(slug='strategic-guide-procuring-authentic-ict-hardware-nigeria').first()
    if not p2:
        BlogPost.objects.create(
            slug='strategic-guide-procuring-authentic-ict-hardware-nigeria',
            title='The Strategic Guide To Procuring Authentic ICT Hardware In Nigeria',
            category=cat_ict,
            author=a_desk,
            author_name='Mark Digital Engineering Desk',
            excerpt='How organizations can eliminate counterfeit electronics risk, ensure genuine warranty coverage, and optimize enterprise IT procurement spending.',
            content='<p>Procuring computing equipment in Nigeria poses notable risks: grey-market re-bagged units, tampered serial numbers, and lack of manufacturer-backed warranties. Ensuring authentic equipment deployment is critical to operational stability.</p>',
            read_time='4 min read',
            status='published',
            featured=False,
            publish_date=now,
        )

    p3 = BlogPost.objects.filter(slug='from-zero-to-youtube-milestone-key-lessons-200k-subscribers').first()
    if not p3:
        BlogPost.objects.create(
            slug='from-zero-to-youtube-milestone-key-lessons-200k-subscribers',
            title='From Zero To YouTube Milestone: Key Lessons From 200,000+ Subscribers',
            category=cat_growth,
            author=a_growth,
            author_name='Mark Digital Growth Team',
            excerpt='Actionable audience retention frameworks, thumbnail psychology, and distribution strategies that built a quarter-million subscriber media asset with Mr. Ben.',
            content='<p>Growing an organic digital audience requires engineering consistency into every single video publish. Reviewing our collaborative milestone with Mr. Ben highlights crucial strategies for sustainable creator channels.</p>',
            read_time='6 min read',
            status='published',
            featured=False,
            publish_date=now,
        )


def rollback(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_blogauthor_avatar_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, rollback),
    ]

