from django.test import TestCase, Client
from django.urls import reverse
from .models import QuoteRequest, Service, CaseStudy, FAQ


class WebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()

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
