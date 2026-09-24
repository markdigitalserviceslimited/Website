from django.core.management.base import BaseCommand
from core.models import Service, CaseStudy, FAQ


class Command(BaseCommand):
    help = 'Seeds initial services, case studies, and FAQs for Mark Digital Services LTD'

    def handle(self, *args, **options):
        # Seed Services
        services_data = [
            {
                'title': 'Website Design & Software Development',
                'slug': 'web-development',
                'short_description': 'Responsive corporate websites, web applications, landing pages, and tailored software solutions engineered for performance, clean aesthetics, and high conversion.',
                'target_audience': 'Businesses, SMEs, Startups, NGOs & Institutions',
                'key_benefit': 'Professional online credibility, seamless user journeys, and robust search visibility.',
                'capabilities_list': 'Custom Responsive Web Design\nWeb Portals & Business Software\nLanding Pages & Conversion Funnels\nSEO-Optimized Code & Fast Page Speed',
                'order': 1,
            },
            {
                'title': 'Social Media Management',
                'slug': 'social-media',
                'short_description': 'Strategic content planning, channel moderation, audience engagement, and performance analytics across YouTube, LinkedIn, Meta, and X to ensure brand consistency.',
                'target_audience': 'Brands, SMEs, Creators, Public Figures & NGOs',
                'key_benefit': 'Consistent organic growth, active customer engagement, and high retention.',
                'capabilities_list': 'Content Calendars & Brand Curation\nAudience Growth & Engagement Strategy\nMulti-Platform Profile Management\nPerformance Analytics & Reporting',
                'order': 2,
            },
            {
                'title': 'Business Promotion & Digital Marketing',
                'slug': 'digital-marketing',
                'short_description': 'Data-driven promotional campaigns designed to expand your market reach, generate qualified customer enquiries, and drive measurable revenue growth.',
                'target_audience': 'SMEs, Startups, Retail, and Growing Enterprises',
                'key_benefit': 'Targeted market visibility and predictable customer acquisition.',
                'capabilities_list': 'Targeted Digital Campaigns\nLead Generation & Growth Funnels\nBrand Awareness & Promotional Roadmaps\nROI & Conversion Rate Optimization',
                'order': 3,
            },
            {
                'title': 'Digital Branding & Creative Content',
                'slug': 'digital-branding',
                'short_description': 'Distinctive visual brand identities, logo systems, corporate guidelines, promotional graphics, and creative assets that set your organization apart from competitors.',
                'target_audience': 'New Businesses, Rebranding Companies & Corporate Teams',
                'key_benefit': 'Memorable visual identity that commands trust and buyer confidence.',
                'capabilities_list': 'Logo & Complete Brand Identity Systems\nMarketing Collateral & Presentation Decks\nHigh-Impact Social Media Visual Kits\nConsistent Visual Brand Guidelines',
                'order': 4,
            },
            {
                'title': 'Technology Training & Skill Development',
                'slug': 'tech-training',
                'short_description': 'Practical, hands-on capacity development and training workshops in modern digital and technology skills for corporate staff, students, and emerging professionals.',
                'target_audience': 'Corporate Teams, Schools, Youth & Learning Communities',
                'key_benefit': 'Equip human capital with tangible digital competence and modern tech skills.',
                'capabilities_list': 'Corporate Digital Workforce Upskilling\nPractical Web & Tech Masterclasses\nDigital Literacy & Productive Tool Training\nCustom Workshops for Teams & Institutions',
                'order': 5,
            },
            {
                'title': 'ICT Equipment & Tech Accessories Supply',
                'slug': 'ict-supply',
                'short_description': 'Procurement, configuration, and supply of verified genuine computers, laptops, networking equipment, peripherals, and office tech accessories with dependable warranty.',
                'target_audience': 'Offices, Educational Institutions, Companies & Professionals',
                'key_benefit': 'Convenient and verified access to authentic hardware tailored to requirements.',
                'capabilities_list': 'Enterprise Laptops, Desktops & Workstations\nNetworking Hardware & Cabling Accessories\nOffice Computing Peripherals & Accessories\nHardware Setup, Testing & Procurement Advisory',
                'order': 6,
            },
        ]

        for s_data in services_data:
            Service.objects.update_or_create(
                slug=s_data['slug'],
                defaults=s_data
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(services_data)} services.'))

        # Seed Case Study
        CaseStudy.objects.update_or_create(
            client_name='Mr. Ben',
            defaults={
                'title': 'YouTube Monetization & Channel Growth Milestone',
                'category': 'YouTube Optimization & Monetization Strategy',
                'milestone_stat': '200,000+ Active Subscribers',
                'objective': 'Strengthen the channel digital presence, improve audience retention and reach, optimize content metadata, and establish sustainable monetization.',
                'outcome': 'The channel successfully scaled beyond 200,000 subscribers with consistent viewer growth, algorithmic optimization, and monetization milestone achievement.',
                'testimonial_quote': 'Mark Digital Services LTD provided practical support that helped us improve our YouTube presence, audience growth and approach to monetization. Seeing the channel grow beyond 200,000 subscribers has been a major milestone.',
                'testimonial_author': 'Mr. Ben (YouTube Creator & Media Channel Partner)',
                'support_areas': 'Channel & Video SEO Optimization\nAudience-Growth & Content Distribution Strategy\nYouTube Compliance & Monetization Guidance\nPerformance Analytics & Retention Tracking',
                'is_featured': True,
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded featured Case Study.'))

        # Seed FAQs
        faqs_data = [
            (
                'How does Mark Digital Services LTD structure project pricing?',
                'We believe in full transparency without hidden fees or unnecessary markups. Because every organization has unique goals, we provide customized quotes based on exact specifications, required deliverables, and technical scope. Once a scope is agreed upon, your quotation is fixed with clear milestones.'
            ),
            (
                'What is the typical delivery turnaround time for a website or branding project?',
                'Most corporate websites, branding systems, and promotional setups are delivered within 2 to 4 weeks from project kickoff and receipt of required assets. Larger custom software or comprehensive ICT hardware rollouts are scheduled in phased milestones.'
            ),
            (
                'Do you deliver services to businesses outside Kogi State across Nigeria and abroad?',
                'Yes! While our registered corporate office is in Kogi State (Ganaja Road), Mark Digital Services LTD operates nationwide across Nigeria (including Lagos, Abuja, Port Harcourt, Kano, etc.) and provides remote digital services to international clients seamlessly via video consultations and collaborative project tools.'
            ),
            (
                'How does the procurement and supply of ICT equipment work?',
                'We work directly with certified distribution partners to source authentic, brand-new laptops, desktops, networking items, and tech peripherals. We inspect, test, and provide vendor warranties, followed by insured nationwide shipping or direct office delivery.'
            ),
            (
                'Can you organize practical digital training for our internal team or institution?',
                'Yes. We design tailored curriculum workshops for corporate organizations, educational institutions, and community groups. Training can be conducted on-site or virtually, focusing on practical real-world skills.'
            ),
            (
                'Is Mark Digital Services LTD a legally registered company?',
                'Yes, Mark Digital Services LTD is an officially incorporated entity with the Corporate Affairs Commission (CAC) of the Federal Republic of Nigeria under RC Number 9435450 (Incorporation Date: 23 March 2026, Tax ID: 2622237423339) as a Private Company Limited by Shares.'
            ),
        ]

        for i, (q, a) in enumerate(faqs_data, start=1):
            FAQ.objects.update_or_create(
                question=q,
                defaults={'answer': a, 'order': i, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(faqs_data)} FAQs.'))
