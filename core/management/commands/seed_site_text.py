from django.core.management.base import BaseCommand
from core.models import SiteText

# (key, label, default value). Every headline, intro paragraph and button
# label on the site has an entry here, so it can be edited from /admin/ ->
# Site text without touching a template. Uses get_or_create: re-running
# this command never overwrites text you've already changed in admin —
# it only adds keys that don't exist yet (e.g. after an update adds a new
# editable spot).
ENTRIES = [
    # --- global -----------------------------------------------------
    ('cta_button_label', 'Everywhere — the main "Request a quote" button text', 'Request a quote'),
    ('brand_subtitle', 'Header & menu — small text under the company name', 'Engineering and supply'),
    ('footer_capabilities_heading', 'Footer — heading above the capabilities list', 'Capabilities'),

    # --- home page ----------------------------------------------------
    ('home_hero_eyebrow', 'Home — small label above the hero headline', 'Industrial supplies and engineering, Tanzania'),
    ('home_hero_h1', 'Home — hero headline', 'Your plant, supplied and running.'),
    ('home_hero_lede', 'Home — hero paragraph (you can use &lt;b&gt;bold&lt;/b&gt;)',
     'Bearings, pneumatic systems, seals, tools and hardware — backed by our own engineering workshop for '
     'machining, fabrication and factory audits. <b>Plus licensed scrap metal trading.</b>'),
    ('home_hero_secondary_cta', 'Home — hero second button label', 'See what we do'),
    ('home_hero_mark_1', 'Home — hero fact, right side, 1st', '<b>Dar es Salaam</b> workshop'),
    ('home_hero_mark_2', 'Home — hero fact, right side, 2nd', '<b>BRELA</b> registered'),
    ('home_hero_mark_3', 'Home — hero fact, right side, 3rd', '<b>8</b> bearing brands stocked'),
    ('home_partners_label', 'Home — caption above the partner logo strip', 'Our partners and clients'),
    ('home_whatwedo_eyebrow', 'Home — "What we do" section label', 'What we do'),
    ('home_whatwedo_h2', 'Home — "What we do" headline', 'Products to keep, services to call on.'),
    ('home_whatwedo_lede', 'Home — "What we do" paragraph',
     'An extensive inventory of industrial components, an engineering workshop behind it, and a licensed '
     'scrap metal trade alongside. Most jobs start with a phone call and a part number — or a photo.'),
    ('home_services_more_label', 'Home — "see full list" button text', 'See the full product and service list'),
    ('home_stat_eyebrow', 'Home — dark stats band label', 'Why plants call us'),
    ('home_stat_h2', 'Home — dark stats band headline', 'One supplier, fewer calls to make.'),
    ('home_recentwork_eyebrow', 'Home — gallery section label', 'Recent work'),
    ('home_recentwork_h2', 'Home — gallery section headline', 'From the workshop floor.'),
    ('home_recentwork_lede', 'Home — gallery section paragraph', 'Machining, panel work and fabrication carried out by our own team.'),
    ('home_gallery_more_label', 'Home — "see full gallery" button text', 'See the full gallery'),
    ('home_howwework_eyebrow', 'Home — "How we work" section label', 'How we work'),
    ('home_howwework_h2', 'Home — "How we work" headline', 'Supplied, machined, or traded.'),
    ('home_howwework_lede', 'Home — "How we work" paragraph', 'Three ways we keep industry moving.'),
    ('home_how1_title', 'Home — "How we work" card 1 title', 'Supply what you need'),
    ('home_how1_body', 'Home — "How we work" card 1 text',
     'An extensive inventory of bearings, pneumatic components, seals, gaskets, tools and hardware — from our own stock.'),
    ('home_how2_title', 'Home — "How we work" card 2 title', 'Build what your plant needs'),
    ('home_how2_body', 'Home — "How we work" card 2 text',
     'Our engineering workshop handles machining, cardan shaft balancing, welding and fabrication, plus '
     'factory audits and hot and cold insulation.'),
    ('home_how3_title', 'Home — "How we work" card 3 title', "Clear what your site doesn't"),
    ('home_how3_body', 'Home — "How we work" card 3 text',
     'Licensed to buy and export dry steel and scrap — fast pick-up, fair pricing, full regulatory compliance.'),
    ('home_cta_h2', 'Home — bottom call-to-action headline', 'Tell us what you need.'),
    ('home_cta_body', 'Home — bottom call-to-action paragraph',
     'Send the part number, a photo, or just describe the job. We will come back with a quote and a realistic timeline.'),

    # --- about page -----------------------------------------------------
    ('about_hero_eyebrow', 'About — small label above the headline', 'The company'),
    ('about_hero_h1', 'About — page headline', 'Industrial supplies and engineering, under one roof.'),
    ('about_hero_lede', 'About — page intro paragraph', 'Operating in Dar es Salaam and beyond since 2022 — a registered wholesaler and licensed scrap metal trader.'),
    ('about_whoweare_eyebrow', 'About — label above the company name', 'Who we are'),
    ('about_stat_eyebrow', 'About — stats band label', 'In short'),
    ('about_stat_h2', 'About — stats band headline', 'What the numbers say.'),
    ('about_cta_h2', 'About — bottom call-to-action headline', 'Ready to talk about your project?'),
    ('about_cta_body', 'About — bottom call-to-action paragraph', 'Tell us about the part, the job, or the load of scrap — we will take it from there.'),

    # --- services page --------------------------------------------------
    ('services_hero_eyebrow', 'Services — small label above the headline', 'What we do'),
    ('services_hero_h1', 'Services — page headline', 'Industrial supply and engineering, end to end.'),
    ('services_hero_lede', 'Services — page intro paragraph', 'From a single O-ring to a fully equipped engineering workshop — one team, one point of contact, one invoice.'),
    ('services_products_eyebrow', 'Services — "Products" section label', 'Products we supply'),
    ('services_products_h2', 'Services — "Products" section headline', 'Bearings, pneumatics, seals, tools and hardware.'),
    ('services_brand_strip_label', 'Services — caption above the bearing-brand logos', 'Bearing brands we stock'),
    ('services_services_eyebrow', 'Services — "Services" section label', 'Services we offer'),
    ('services_services_h2', 'Services — "Services" section headline', 'Engineering, audits and scrap metal trading.'),
    ('services_cta_h2', 'Services — bottom call-to-action headline', 'Not sure which of these you need?'),
    ('services_cta_body', 'Services — bottom call-to-action paragraph', 'Describe the part or the job and we will tell you what it takes.'),

    # --- our work page ----------------------------------------------------
    ('work_hero_eyebrow', 'Our work — small label above the headline', 'Recent work'),
    ('work_hero_h1', 'Our work — page headline', 'From the workshop floor.'),
    ('work_hero_lede', 'Our work — page intro paragraph', 'Overhauls, fabrication and repairs completed on site and in our workshop for clients across Tanzania.'),
    ('work_partners_label', 'Our work — caption above the partner logo strip', 'Partners and clients we have worked with'),
    ('work_cta_h2', 'Our work — bottom call-to-action headline', "Let's talk about your next job."),
    ('work_cta_body', 'Our work — bottom call-to-action paragraph', 'Send us the details and we will come back with a quote and a realistic timeline.'),

    # --- contact page -------------------------------------------------
    ('contact_hero_eyebrow', 'Contact — small label above the headline', 'Get in touch'),
    ('contact_hero_h1', 'Contact — page headline', 'Tell us what your line needs.'),
    ('contact_hero_lede', 'Contact — page intro paragraph', 'Parts, a repair, or a full engineering project — send the details and we will come back with a quote.'),
    ('contact_details_eyebrow', 'Contact — label above the company name', 'Contact details'),
    ('contact_form_intro', 'Contact — line above the quote form', 'The more detail you send, the faster the quote comes back.'),
]


class Command(BaseCommand):
    help = 'Seed every editable headline/paragraph/button label as a Site text entry (safe to re-run; never overwrites existing text).'

    def handle(self, *args, **options):
        created = 0
        for key, label, value in ENTRIES:
            _, was_created = SiteText.objects.get_or_create(key=key, defaults={'label': label, 'value': value})
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Site text ready — added {created} new entries ({len(ENTRIES)} total defined).'))
