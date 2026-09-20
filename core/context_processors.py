from .models import CompanyInfo, SiteText


def company_info(request):
    company = CompanyInfo.objects.first()
    return {'company': company}


def site_text(request):
    """Every editable text snippet, as a dict: {{ site_text.KEY }}.
    A missing key just renders empty, so `{{ site_text.some_key|default:"..." }}`
    in a template always has a safe fallback even before this is seeded."""
    texts = {t.key: t.value for t in SiteText.objects.all()}
    return {'site_text': texts}
