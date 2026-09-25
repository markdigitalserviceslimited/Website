from django.conf import settings


def site_settings(request):
    """
    Expose centralized environment constants to all templates.
    """
    return {
        'COMPANY_NAME': getattr(settings, 'COMPANY_NAME', 'Mark Digital Services LTD'),
        'COMPANY_LEGAL_ENTITY': getattr(settings, 'COMPANY_LEGAL_ENTITY', 'Private Company Limited by Shares'),
        'COMPANY_DIRECTOR': getattr(settings, 'COMPANY_DIRECTOR', 'Akor Mark Akoji'),
        'COMPANY_OFFICE_ADDRESS': getattr(settings, 'COMPANY_OFFICE_ADDRESS', '2, Rock Garden Avenue, Along Ganaja Road, Kogi State, Nigeria'),
        'COMPANY_PHONE': getattr(settings, 'COMPANY_PHONE', '+234 811 789 7778'),
        'COMPANY_PHONE_RAW': getattr(settings, 'COMPANY_PHONE_RAW', '2348117897778'),
        'COMPANY_WHATSAPP': getattr(settings, 'COMPANY_WHATSAPP', '+234 811 789 7778'),
        'COMPANY_WHATSAPP_URL': getattr(settings, 'COMPANY_WHATSAPP_URL', 'https://wa.me/2348117897778?text=Hello%20Mark%20Digital%20Services%20LTD%2C%20I%20would%20like%20to%20discuss%20a%20project.'),
        'COMPANY_EMAIL': getattr(settings, 'COMPANY_EMAIL', 'markdigitalserviceslimited@gmail.com'),
        'NOTIFICATION_EMAIL': getattr(settings, 'NOTIFICATION_EMAIL', 'markdigitalserviceslimited@gmail.com'),
        'LINKEDIN_URL': getattr(settings, 'LINKEDIN_URL', 'https://www.linkedin.com/company/mdg-ltd/'),
        'FACEBOOK_URL': getattr(settings, 'FACEBOOK_URL', 'https://web.facebook.com/mark.akor.210789/'),
        'WORKING_HOURS_WEEKDAY': getattr(settings, 'WORKING_HOURS_WEEKDAY', 'Monday – Friday: 9:00 AM – 5:00 PM WAT'),
        'WORKING_HOURS_WEEKEND': getattr(settings, 'WORKING_HOURS_WEEKEND', 'Saturday: 10:00 AM – 2:00 PM WAT'),
        'SITE_URL': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
    }
