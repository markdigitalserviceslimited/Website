from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import (
    QuoteRequest, Service, CaseStudy, FAQ,
    BlogCategory, BlogPost, Testimonial,
    BlogAuthor, AuthorSocialLink
)


class WebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.testimonial = Testimonial.objects.create(
            client_name='Mr. Ben',
            client_title_or_role='YouTube Creator & Media Partner',
            organization='200K+ Milestone Channel',
            service_category='YouTube Growth',
            quote='Mark Digital Services LTD provided practical support that helped us grow.',
            avatar_initial='B',
            rating=5,
            verified=True,
            order=1,
            is_active=True
        )

    def test_home_page_loads_with_required_elements(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MARK DIGITAL')
        self.assertContains(response, 'Incorporated Nigerian Firm')
        self.assertContains(response, '+234 811 789 7778')
        self.assertContains(response, 'markdigitalserviceslimited@gmail.com')
        self.assertContains(response, 'Mr. Ben')
        self.assertContains(response, '200,000+ Subscribers')
        self.assertContains(response, 'Akor Mark Akoji')
        self.assertContains(response, 'Ganaja Road')
        self.assertContains(response, 'Website Design &amp; Software Development')
        self.assertContains(response, 'ICT Equipment &amp; Tech Accessories Supply')


    def test_quote_request_submission_regular(self):
        data = {
            'full_name': 'Chinedu Eze',
            'business_name': 'Eze Logistics Ltd',
            'email': 'chinedu@ezelogistics.ng',
            'phone_or_whatsapp': '+2348012345678',
            'service_needed': 'web_development',
            'project_description': 'Need a corporate web portal and booking logistics platform.',
            'estimated_budget': 'tier_2',
            'timeline': 'normal',
        }
        response = self.client.post(reverse('core:home'), data)
        self.assertEqual(response.status_code, 302)  # Redirects with flash message
        self.assertTrue(QuoteRequest.objects.filter(email='chinedu@ezelogistics.ng').exists())
        quote = QuoteRequest.objects.get(email='chinedu@ezelogistics.ng')
        self.assertEqual(quote.full_name, 'Chinedu Eze')
        self.assertEqual(quote.status, 'new')

    def test_quote_request_submission_ajax(self):
        data = {
            'full_name': 'Amina Bello',
            'business_name': 'Bello Edu Tech',
            'email': 'amina@belloedutech.org',
            'phone_or_whatsapp': '+2348098765432',
            'service_needed': 'tech_training',
            'project_description': 'In-house digital skills and programming training for 20 team members.',
            'estimated_budget': 'tier_3',
            'timeline': 'immediate',
        }
        response = self.client.post(
            reverse('core:home'),
            data,
            headers={'x-requested-with': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(QuoteRequest.objects.filter(email='amina@belloedutech.org').exists())

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Mark Digital Services LTD')
        self.assertContains(response, 'Akor Mark Akoji')
        self.assertContains(response, 'Private Company Limited by Shares')

    def test_services_page(self):
        response = self.client.get(reverse('core:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Our Core Services')
        self.assertContains(response, 'Website Design &amp; Software Development')

    def test_portfolio_page(self):
        response = self.client.get(reverse('core:portfolio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Portfolio & Case Studies')
        self.assertContains(response, 'Mr. Ben')
        self.assertContains(response, '200,000+ Active Subscribers')

    def test_contact_page(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact & Request a Quote')
        self.assertContains(response, '+234 811 789 7778')

    def test_privacy_policy_page(self):
        response = self.client.get(reverse('core:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Privacy Policy')
        self.assertContains(response, 'Mark Digital Services LTD')

    def test_terms_page(self):
        response = self.client.get(reverse('core:terms'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Terms & Conditions')
        self.assertContains(response, 'Akor Mark Akoji')

    def test_blog_list_and_detail_views(self):
        cat = BlogCategory.objects.create(name='Tech Trends', slug='tech-trends')
        post = BlogPost.objects.create(
            title='The Future of Enterprise Software in Nigeria',
            slug='future-of-enterprise-software-nigeria',
            category=cat,
            author_name='Akor Mark Akoji',
            excerpt='A thorough analysis of cloud systems, API integrations, and tech productivity.',
            content='<p>Full article body on software systems and enterprise performance.</p>',
            read_time='4 min read',
            status='published',
            publish_date=timezone.now(),
        )

        # 1. Test Blog List View
        list_resp = self.client.get(reverse('core:blog_list'))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, 'The Future Of Enterprise Software In Nigeria')
        self.assertContains(list_resp, 'Tech Trends')

        # 2. Test Category Filter
        cat_resp = self.client.get(reverse('core:blog_list') + '?category=tech-trends')
        self.assertEqual(cat_resp.status_code, 200)
        self.assertContains(cat_resp, 'The Future Of Enterprise Software In Nigeria')

        # 3. Test Search Query
        search_resp = self.client.get(reverse('core:blog_list') + '?q=Enterprise')
        self.assertEqual(search_resp.status_code, 200)
        self.assertContains(search_resp, 'The Future Of Enterprise Software In Nigeria')

        # 4. Test Blog Detail View & View Count Increment
        initial_views = post.view_count
        detail_resp = self.client.get(reverse('core:blog_detail', kwargs={'slug': post.slug}))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, 'The Future Of Enterprise Software In Nigeria')
        self.assertContains(detail_resp, 'Full article body on software systems')

        post.refresh_from_db()
        self.assertEqual(post.view_count, initial_views + 1)

    def test_auto_capitalization_and_dynamic_authors(self):
        # 1. Category name auto-capitalization
        cat = BlogCategory.objects.create(name='  artificial intelligence & cloud computing  ', slug='ai-cloud')
        self.assertEqual(cat.name, 'Artificial Intelligence & Cloud Computing')

        # 2. Author name & role auto-capitalization + initials generation
        author = BlogAuthor.objects.create(
            name='  samuel chinedu  ',
            slug='samuel-chinedu',
            role_or_title='  senior cloud engineer  ',
            bio='Expert in distributed backend systems.',
        )
        self.assertEqual(author.name, 'Samuel Chinedu')
        self.assertEqual(author.role_or_title, 'Senior Cloud Engineer')
        self.assertEqual(author.avatar_initial, 'SC')

        # 3. Dynamic Author Social Media Links
        from .models import AuthorSocialLink
        social_link = AuthorSocialLink.objects.create(
            author=author,
            platform='linkedin',
            url='https://linkedin.com/in/samuelchinedu',
            order=1
        )
        self.assertEqual(author.social_links.count(), 1)
        self.assertEqual(str(social_link), 'Samuel Chinedu - LinkedIn')

        # 4. Blog Post title auto-capitalization & dynamic author sync
        post = BlogPost.objects.create(
            title='  building scalable microservices with django and python  ',
            slug='building-scalable-microservices',
            category=cat,
            author=author,
            excerpt='Deep dive into high performance web APIs.',
            content='<p>Microservices architecture fundamentals and real-world benchmarks.</p>',
            status='published',
            publish_date=timezone.now(),
        )
        self.assertEqual(post.title, 'Building Scalable Microservices With Django And Python')
        self.assertEqual(post.author_name, 'Samuel Chinedu')
        self.assertEqual(post.get_author_display(), 'Samuel Chinedu')

        # 5. Detail view renders author, bio, and social media links
        detail_resp = self.client.get(reverse('core:blog_detail', kwargs={'slug': post.slug}))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, 'Samuel Chinedu')
        self.assertContains(detail_resp, 'Senior Cloud Engineer')
        self.assertContains(detail_resp, 'Expert in distributed backend systems.')
        self.assertContains(detail_resp, 'https://linkedin.com/in/samuelchinedu')
        self.assertContains(detail_resp, 'SC')

        # 6. List view renders author
        list_resp = self.client.get(reverse('core:blog_list'))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, 'Building Scalable Microservices With Django And Python')
        self.assertContains(list_resp, 'Samuel Chinedu')

