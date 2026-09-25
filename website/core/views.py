import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import QuoteRequest, Service, CaseStudy, FAQ
from .forms import QuoteRequestForm

logger = logging.getLogger(__name__)


def send_quote_notification(quote):
    """
    Sends an email notification to company Gmail when a quote is submitted.
    Fails silently so form submission and UX never break if SMTP is unconfigured.
    """
    subject = f"New Project Quote Request: {quote.full_name} ({quote.get_service_needed_display()})"
    message = f"""You have received a new project quote request on Mark Digital Services LTD website:

Client Details:
- Name: {quote.full_name}
- Business / Organization: {quote.business_name or 'N/A'}
- Email: {quote.email}
- Phone / WhatsApp: {quote.phone_or_whatsapp}

Project Scope:
- Service Needed: {quote.get_service_needed_display()}
- Estimated Budget: {quote.get_estimated_budget_display()}
- Expected Timeline: {quote.get_timeline_display()}

Project Description:
{quote.project_description}

---
Submitted at: {quote.created_at.strftime('%Y-%m-%d %H:%M:%S UTC') if quote.created_at else 'Just now'}
Quick WhatsApp Link: https://wa.me/{quote.phone_or_whatsapp.replace('+', '').replace(' ', '')}
"""
    try:
        recipient = getattr(settings, 'NOTIFICATION_EMAIL', 'markdigitalserviceslimited@gmail.com')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', recipient)
        # Send notification email
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient],
            fail_silently=True,
        )
    except Exception as e:
        logger.warning(f"Could not send email notification for quote {quote.id}: {e}")


def get_default_services():
    return [
        {
            'title': 'Website Design & Software Development',
            'slug': 'web-development',
            'short_description': 'Responsive corporate websites, web applications, landing pages, and tailored software solutions engineered for performance, clean aesthetics, and conversion.',
            'target_audience': 'Businesses, SMEs, Startups, NGOs & Institutions',
            'key_benefit': 'Professional online credibility, seamless user journeys, and robust search visibility.',
            'capabilities': [
                'Custom Responsive Web Design',
                'Web Portals & Business Software',
                'Landing Pages & Conversion Funnels',
                'SEO-Optimized Code & Fast Page Speed',
            ],
            'icon': 'globe',
        },
        {
            'title': 'Social Media Management',
            'slug': 'social-media',
            'short_description': 'Strategic content planning, channel moderation, audience engagement, and performance analytics across YouTube, LinkedIn, Meta, and X to ensure brand consistency.',
            'target_audience': 'Brands, SMEs, Creators, Public Figures & NGOs',
            'key_benefit': 'Consistent organic growth, active customer engagement, and high retention.',
            'capabilities': [
                'Content Calendars & Brand Curation',
                'Audience Growth & Engagement Strategy',
                'Multi-Platform Profile Management',
                'Performance Analytics & Reporting',
            ],
            'icon': 'share-2',
        },
        {
            'title': 'Business Promotion & Digital Marketing',
            'slug': 'digital-marketing',
            'short_description': 'Data-driven promotional campaigns designed to expand your market reach, generate qualified customer enquiries, and drive measurable revenue growth.',
            'target_audience': 'SMEs, Startups, Retail, and Growing Enterprises',
            'key_benefit': 'Targeted market visibility and predictable customer acquisition.',
            'capabilities': [
                'Targeted Digital Campaigns',
                'Lead Generation & Growth Funnels',
                'Brand Awareness & Promotional Roadmaps',
                'ROI & Conversion Rate Optimization',
            ],
            'icon': 'trending-up',
        },
        {
            'title': 'Digital Branding & Creative Content',
            'slug': 'digital-branding',
            'short_description': 'Distinctive visual brand identities, logo systems, corporate guidelines, promotional graphics, and creative assets that set your organization apart from competitors.',
            'target_audience': 'New Businesses, Rebranding Companies & Corporate Teams',
            'key_benefit': 'Memorable visual identity that commands trust and buyer confidence.',
            'capabilities': [
                'Logo & Complete Brand Identity Systems',
                'Marketing Collateral & Presentation Decks',
                'High-Impact Social Media Visual Kits',
                'Consistent Visual Brand Guidelines',
            ],
            'icon': 'palette',
        },
        {
            'title': 'Technology Training & Skill Development',
            'slug': 'tech-training',
            'short_description': 'Practical, hands-on capacity development and training workshops in modern digital and technology skills for corporate staff, students, and emerging professionals.',
            'target_audience': 'Corporate Teams, Schools, Youth & Learning Communities',
            'key_benefit': 'Equip human capital with tangible digital competence and modern tech skills.',
            'capabilities': [
                'Corporate Digital Workforce Upskilling',
                'Practical Web & Tech Masterclasses',
                'Digital Literacy & Productive Tool Training',
                'Custom Workshops for Teams & Institutions',
            ],
            'icon': 'graduation-cap',
        },
        {
            'title': 'ICT Equipment & Tech Accessories Supply',
            'slug': 'ict-supply',
            'short_description': 'Procurement, configuration, and supply of verified genuine computers, laptops, networking equipment, peripherals, and office tech accessories with dependable warranty.',
            'target_audience': 'Offices, Educational Institutions, Companies & Professionals',
            'key_benefit': 'Convenient and verified access to authentic hardware tailored to requirements.',
            'capabilities': [
                'Enterprise Laptops, Desktops & Workstations',
                'Networking Hardware & Cabling Accessories',
                'Office Computing Peripherals & Accessories',
                'Hardware Setup, Testing & Procurement Advisory',
            ],
            'icon': 'cpu',
        },
    ]


def get_default_faqs():
    return [
        {
            'question': 'How does Mark Digital Services LTD structure project pricing?',
            'answer': 'We believe in full transparency without hidden fees or unnecessary markups. Because every organization has unique goals, we provide customized quotes based on exact specifications, required deliverables, and technical scope. Once a scope is agreed upon, your quotation is fixed with clear milestones.'
        },
        {
            'question': 'What is the typical delivery turnaround time for a website or branding project?',
            'answer': 'Most corporate websites, branding systems, and promotional setups are delivered within 2 to 4 weeks from project kickoff and receipt of required assets. Larger custom software or comprehensive ICT hardware rollouts are scheduled in phased milestones.'
        },
        {
            'question': 'Do you deliver services to businesses outside Kogi State across Nigeria and abroad?',
            'answer': 'Yes! While our registered corporate office is in Kogi State (Ganaja Road), Mark Digital Services LTD operates nationwide across Nigeria (including Lagos, Abuja, Port Harcourt, Kano, etc.) and provides remote digital services to international clients seamlessly via video consultations and collaborative project tools.'
        },
        {
            'question': 'How does the procurement and supply of ICT equipment work?',
            'answer': 'We work directly with certified distribution partners to source authentic, brand-new laptops, desktops, networking items, and tech peripherals. We inspect, test, and provide vendor warranties, followed by insured nationwide shipping or direct office delivery.'
        },
        {
            'question': 'Can you organize practical digital training for our internal team or institution?',
            'answer': 'Yes. We design tailored curriculum workshops for corporate organizations, educational institutions, and community groups. Training can be conducted on-site or virtually, focusing on practical real-world skills.'
        },
        {
            'question': 'Is Mark Digital Services LTD a legally registered company?',
            'answer': 'Yes, Mark Digital Services LTD is an officially incorporated entity in the Federal Republic of Nigeria, operating as a Private Company Limited by Shares with full legal standing.'
        },
    ]


def home_view(request):
    # Fetch DB services or fallback
    services_qs = Service.objects.filter(is_active=True)
    if services_qs.exists():
        services_data = [
            {
                'title': s.title,
                'slug': s.slug,
                'short_description': s.short_description,
                'target_audience': s.target_audience,
                'key_benefit': s.key_benefit,
                'capabilities': s.get_capabilities(),
                'icon': 'globe'
            }
            for s in services_qs
        ]
    else:
        services_data = get_default_services()

    # Fetch DB case studies or fallback
    case_studies = CaseStudy.objects.all()
    if not case_studies.exists():
        featured_case = {
            'client_name': 'Mr. Ben',
            'title': 'YouTube Monetization & Channel Growth Milestone',
            'milestone_stat': '200,000+ Subscribers',
            'category': 'YouTube Optimization & Monetization Strategy',
            'objective': 'Strengthen the channel digital presence, improve audience retention and reach, optimize content metadata, and establish sustainable monetization.',
            'outcome': 'The channel successfully scaled beyond 200,000 subscribers with consistent viewer growth, algorithmic optimization, and monetization milestone achievement.',
            'testimonial_quote': 'Mark Digital Services LTD provided practical support that helped us improve our YouTube presence, audience growth and approach to monetization. Seeing the channel grow beyond 200,000 subscribers has been a major milestone.',
            'testimonial_author': 'Mr. Ben (YouTube Creator & Media Channel Partner)',
            'support_areas': [
                'Channel & Video SEO Optimization',
                'Audience-Growth & Content Distribution Strategy',
                'YouTube Compliance & Monetization Guidance',
                'Performance Analytics & Retention Tracking',
            ]
        }
    else:
        first_case = case_studies.first()
        featured_case = {
            'client_name': first_case.client_name,
            'title': first_case.title,
            'milestone_stat': first_case.milestone_stat,
            'category': first_case.category,
            'objective': first_case.objective,
            'outcome': first_case.outcome,
            'testimonial_quote': first_case.testimonial_quote,
            'testimonial_author': first_case.testimonial_author,
            'support_areas': first_case.get_support_areas(),
        }

    # Fetch FAQs
    faqs_qs = FAQ.objects.filter(is_active=True)
    if faqs_qs.exists():
        faqs_data = [{'question': f.question, 'answer': f.answer} for f in faqs_qs]
    else:
        faqs_data = get_default_faqs()

    form = QuoteRequestForm()

    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            send_quote_notification(quote)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f'Thank you, {quote.full_name}! Your quote request has been received. Our team will review your project details and respond via email or WhatsApp within 24 hours.'
                })
            messages.success(
                request,
                f'Thank you, {quote.full_name}! Your project request has been submitted successfully. A representative will contact you shortly.'
            )
            return redirect('/#quote-section')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors.get_json_data()
                }, status=400)
            messages.error(request, 'Please check the form fields and correct the highlighted errors.')

    context = {
        'services': services_data,
        'featured_case': featured_case,
        'faqs': faqs_data,
        'form': form,
    }
    return render(request, 'home.html', context)


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


def terms_view(request):
    return render(request, 'terms.html')


def about_view(request):
    context = {
        'page_title': 'About Us & Corporate Governance | Mark Digital Services LTD',
    }
    return render(request, 'about.html', context)


def services_view(request):
    services_qs = Service.objects.filter(is_active=True)
    if services_qs.exists():
        services_data = [
            {
                'title': s.title,
                'slug': s.slug,
                'short_description': s.short_description,
                'target_audience': s.target_audience,
                'key_benefit': s.key_benefit,
                'capabilities': s.get_capabilities(),
                'icon': 'globe'
            }
            for s in services_qs
        ]
    else:
        services_data = get_default_services()

    context = {
        'services': services_data,
        'page_title': 'Our Services | Mark Digital Services LTD',
    }
    return render(request, 'services.html', context)


def portfolio_view(request):
    case_studies = CaseStudy.objects.all()
    if not case_studies.exists():
        featured_case = {
            'client_name': 'Mr. Ben',
            'title': 'YouTube Monetization & Channel Growth Milestone',
            'milestone_stat': '200,000+ Active Subscribers',
            'category': 'YouTube Optimization & Monetization Strategy',
            'objective': 'Strengthen the channel digital presence, improve audience retention and reach, optimize content metadata, and establish sustainable monetization.',
            'outcome': 'The channel successfully scaled beyond 200,000 subscribers with consistent viewer growth, algorithmic optimization, and monetization milestone achievement.',
            'testimonial_quote': 'Mark Digital Services LTD provided practical support that helped us improve our YouTube presence, audience growth and approach to monetization. Seeing the channel grow beyond 200,000 subscribers has been a major milestone.',
            'testimonial_author': 'Mr. Ben (YouTube Creator & Media Channel Partner)',
            'support_areas': [
                'Channel & Video SEO Optimization',
                'Audience-Growth & Content Distribution Strategy',
                'YouTube Compliance & Monetization Guidance',
                'Performance Analytics & Retention Tracking',
            ]
        }
        all_cases = [featured_case]
    else:
        all_cases = [
            {
                'client_name': c.client_name,
                'title': c.title,
                'milestone_stat': c.milestone_stat,
                'category': c.category,
                'objective': c.objective,
                'outcome': c.outcome,
                'testimonial_quote': c.testimonial_quote,
                'testimonial_author': c.testimonial_author,
                'support_areas': c.get_support_areas(),
            }
            for c in case_studies
        ]
        featured_case = all_cases[0]

    context = {
        'featured_case': featured_case,
        'all_cases': all_cases,
        'page_title': 'Portfolio & Client Case Studies | Mark Digital Services LTD',
    }
    return render(request, 'portfolio.html', context)


def contact_view(request):
    initial = {}
    service_param = request.GET.get('service')
    if service_param:
        initial['service_needed'] = service_param.replace('-', '_')
    form = QuoteRequestForm(initial=initial)
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            send_quote_notification(quote)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f'Thank you, {quote.full_name}! Your quote request has been received. Our team will review your project details and respond via email or WhatsApp within 24 hours.'
                })
            messages.success(
                request,
                f'Thank you, {quote.full_name}! Your project request has been submitted successfully. A representative will contact you shortly.'
            )
            return redirect('core:contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors.get_json_data()
                }, status=400)
            messages.error(request, 'Please check the form fields and correct the highlighted errors.')

    context = {
        'form': form,
        'page_title': 'Contact & Request a Quote | Mark Digital Services LTD',
    }
    return render(request, 'contact.html', context)

