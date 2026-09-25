from django import forms
from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'full_name',
            'business_name',
            'email',
            'phone_or_whatsapp',
            'service_needed',
            'project_description',
            'estimated_budget',
            'timeline',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white placeholder-slate-400',
                'placeholder': 'Your Full Name (e.g. John Doe)',
                'required': True,
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white placeholder-slate-400',
                'placeholder': 'Business / Organization Name (Optional)',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white placeholder-slate-400',
                'placeholder': 'you@company.com',
                'required': True,
            }),
            'phone_or_whatsapp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white placeholder-slate-400',
                'placeholder': '+234 811 789 7778',
                'required': True,
            }),
            'service_needed': forms.Select(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white',
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white placeholder-slate-400 resize-y',
                'rows': 4,
                'placeholder': 'Tell us about your project, goals, key deliverables, and any specific requirements...',
                'required': True,
            }),
            'estimated_budget': forms.Select(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white',
            }),
            'timeline': forms.Select(attrs={
                'class': 'w-full px-4 py-3 min-h-[44px] rounded-lg border border-slate-200 focus:ring-2 focus:ring-brandBlue focus:border-brandBlue transition-colors text-brandDark text-sm bg-white',
            }),
        }
