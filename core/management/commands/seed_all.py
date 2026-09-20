"""
Seed the whole site with the client's own real content:

    python manage.py seed_all

Runs seed_company (real company profile, phone numbers, and the full
15-item product/service list, all sourced from the client's own
documents — about_company.docx and WEBSITEE_CONTENTS.docx), then adds:

- Product/service icon photos  (from WEBSITEE_CONTENTS.docx)
- Bearing brand logos          (NACHI, INA, Timken, NTN, Koyo, FAG, SKF, NSK)
- Gallery photos               (4 real, Tryvis-branded workshop photos)
- Hero slides                  (the same 4 real photos, cross-fading)

Every image comes from core/seed_assets/ — real photos the client supplied
in their own WEBSITEE_CONTENTS.docx, extracted and lightly resized/
compressed for the web. Nothing here is stock photography or generated
placeholder art, and Partner is intentionally left untouched — the client
manages that list themselves in /admin/.

Safe to re-run: skips anything that already exists. Use --force to wipe
and redo the icon/brand/gallery/hero images only (company profile and the
product/service text are never deleted by this command).
"""
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.models import ServiceCategory, Brand, GalleryImage, HeroSlide

ASSETS = Path(__file__).resolve().parent.parent.parent / 'seed_assets'

PRODUCT_ICONS = {
    'bearings': 'products/bearings.jpg',
    'pneumatic-systems': 'products/pneumatic.jpg',
    'pressure-gauges': 'products/pressure_gauge.jpg',
    'industrial-tools': 'products/industrial_tools.jpg',
    'mechanical-seals': 'products/mechanical_seal.jpg',
    'oil-seals': 'products/oil_seal.jpg',
    'fasteners': 'products/fasteners.jpg',
    'o-rings': 'products/o_rings.jpg',
    'sms-union-gaskets': 'products/sms_gasket.jpg',
    'cleaning-sanitary-equipment': 'products/cleaning_equipment.jpg',
    'hardware': 'products/hardware.jpg',
    'engineering-workshop': 'services/engineering_workshop.jpg',
    'hot-cold-insulation': 'services/insulation.jpg',
    'factory-audits': 'services/factory_audit.jpg',
    'scrap-metal-trading': 'services/scrap_metal.jpg',
}

BRANDS = [
    ('NACHI', 'brands/nachi.jpg'),
    ('INA', 'brands/ina.jpg'),
    ('Timken', 'brands/timken.jpg'),
    ('NTN', 'brands/ntn.jpg'),
    ('Koyo', 'brands/koyo.jpg'),
    ('FAG', 'brands/fag.jpg'),
    ('SKF', 'brands/skf.jpg'),
    ('NSK', 'brands/nsk.jpg'),
]

# All four are real Tryvis Investments photos (staff in branded PPE, the
# company name visible on vests/equipment) pulled from WEBSITEE_CONTENTS.docx.
GALLERY = [
    ('Machining in the workshop', 'workshop', 'gallery/workshop-1.jpg'),
    ('Preparing a control panel on the bench', 'workshop', 'gallery/workshop-2.jpg'),
    ('Panel wiring and testing', 'workshop', 'gallery/workshop-3.jpg'),
    ('Welding work in progress', 'workshop', 'gallery/workshop-4.jpg'),
]

HERO = ['hero/hero-1.jpg', 'hero/hero-2.jpg', 'hero/hero-3.jpg']


def _file(rel_path):
    return ContentFile((ASSETS / rel_path).read_bytes(), name=Path(rel_path).name)


class Command(BaseCommand):
    help = 'Seed the entire site with real content: company profile, products/services, brand logos, gallery and hero photos.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Delete existing Brand/GalleryImage/HeroSlide rows and service icon images, then regenerate them.',
        )

    def handle(self, *args, **options):
        call_command('seed_company')
        call_command('seed_site_text')

        if options['force']:
            Brand.objects.all().delete()
            GalleryImage.objects.all().delete()
            HeroSlide.objects.all().delete()
            for sc in ServiceCategory.objects.exclude(icon_image=''):
                sc.icon_image.delete(save=True)
            self.stdout.write('Cleared existing brands, gallery, hero slides and service icons (--force).')

        # ---- service/product icons -----------------------------------
        updated = 0
        for slug, rel in PRODUCT_ICONS.items():
            try:
                sc = ServiceCategory.objects.get(slug=slug)
            except ServiceCategory.DoesNotExist:
                continue
            if sc.icon_image:
                continue
            sc.icon_image.save(Path(rel).name, _file(rel), save=True)
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Set {updated} product/service icon photos.') if updated
                           else 'Service icons already set — skipping.')

        # ---- brand logos ------------------------------------------------
        if Brand.objects.exists():
            self.stdout.write('Brands already exist — skipping (use --force to regenerate).')
        else:
            for i, (name, rel) in enumerate(BRANDS):
                b = Brand(name=name, order=i)
                b.logo.save(Path(rel).name, _file(rel), save=True)
            self.stdout.write(self.style.SUCCESS(f'Created {len(BRANDS)} brand logos.'))

        # ---- gallery ("Our work") ----------------------------------------
        if GalleryImage.objects.exists():
            self.stdout.write('Gallery already has images — skipping (use --force to regenerate).')
        else:
            for i, (title, category, rel) in enumerate(GALLERY):
                gi = GalleryImage(title=title, category=category, order=i)
                gi.image.save(Path(rel).name, _file(rel), save=True)
            self.stdout.write(self.style.SUCCESS(
                f'Created {len(GALLERY)} gallery photos. (Only 4 real photos were supplied — add more '
                'any time via /admin/.)'
            ))

        # ---- hero slides ---------------------------------------------
        if HeroSlide.objects.exists():
            self.stdout.write('Hero slides already exist — skipping (use --force to regenerate).')
        else:
            for i, rel in enumerate(HERO):
                hs = HeroSlide(order=i, is_active=True)
                hs.image.save(Path(rel).name, _file(rel), save=True)
            self.stdout.write(self.style.SUCCESS(f'Created {len(HERO)} hero slides from real workshop photos.'))

        self.stdout.write(self.style.SUCCESS(
            'Site fully seeded with real content. Partner logos were left untouched, as requested.'
        ))
