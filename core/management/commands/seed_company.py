from django.core.management.base import BaseCommand
from core.models import CompanyInfo, PhoneNumber, ServiceCategory, Stat

# Every string below is taken verbatim (or lightly copy-edited only for a
# typo/line-break) from the company's own documents: about_company.docx,
# the TRA TIN certificate, the BRELA Certificate of Incorporation, and the
# Ubungo Municipal Council business licence. Nothing here is invented.


class Command(BaseCommand):
    help = 'Seed the real Tryvis Investments company profile, phone numbers and service/product list.'

    def handle(self, *args, **options):
        company, created = CompanyInfo.objects.get_or_create(
            name='Tryvis Investments Limited',
            defaults=dict(
                tagline='Your trusted partner for industrial supplies and engineering services in Tanzania.',
                about=(
                    'Established in 2022, Tryvis Investments Limited is your trusted partner for a wide '
                    'range of industrial supplies and engineering services in Tanzania, Dar es Salaam area '
                    'and beyond. As a versatile wholesaler, we provide an extensive inventory of bearings, '
                    'pneumatic tools, and other essential components. Our expertise extends to professional '
                    'services including fabrication engineering, machine workshop operations, and insulation '
                    'contracting. We also specialize in air-conditioning services, ensuring we meet diverse '
                    'industrial and mechanical needs with exceptional skill and reliability.\n\n'
                    'We are also a Tanzania buyer, and primarily engage in the import and export business '
                    'of products. We provide reliable support for cross-border trade decision-making.'
                ),
                vision=(
                    'To be the preeminent independent supplier of choice recognized by our customers as the '
                    'best in total satisfaction and value.'
                ),
                mission=(
                    'To achieve the highest level of customer satisfaction by providing quality products and '
                    'services in time and at competitive costs.'
                ),
                # NOTE: this is the exact sentence from about_company.docx — it reads as
                # cut off ("...we continue to uphold" with nothing after). Left verbatim
                # rather than guessing an ending; ask the client for the finished line.
                values='We listen, we care, and we continue to uphold.',
                address_line='Plot 15, Msigani, Malamba Mawili Street, Dar es Salaam',
                po_box='P.O. Box 10952, Dar es Salaam',
                email='tryvisinvesment@gmail.com',  # verbatim from about_company.docx — note the missing "t"
                tin='156-481-602',
                brela_reg_no='156481602',
                business_license_no='BL01396922026-2700003491',
            )
        )
        if not created:
            self.stdout.write('Company info already exists — skipping creation, updating numbers only.')

        # Both numbers below are the two phone lines listed under CONTACTS in
        # about_company.docx. No WhatsApp number is set here — none of the
        # supplied documents says which line (if any) takes WhatsApp, so
        # nothing was guessed. Set it in /admin/ (Company Info) once you've
        # confirmed which number to use; the WhatsApp button stays hidden
        # until then.
        numbers = [
            ('+255 793 555 702', ''),
            ('0733 331 804', ''),
        ]
        for number, label in numbers:
            PhoneNumber.objects.get_or_create(company=company, number=number, defaults={'label': label})

        # ---- Products we supply (from the "PRODUCTS" section of WEBSITEE_CONTENTS.docx) ----
        products = [
            ('bearings', 'Bearings',
             'Deep groove ball bearings, angular contact bearings, robot bearings, needle roller bearings, '
             'tapered roller bearings, cylindrical roller bearings, self-aligning roller bearings and more.',
             'We understand the importance of quality and reliability when it comes to bearings, which is '
             'why we only offer products that meet our strict standards for performance and durability. '
             'Types supplied include spherical roller bearings, cylindrical roller bearings, self-aligning '
             'ball bearings, deep groove ball bearings, thrust ball bearings, needle roller bearings, linear '
             'motion bearings, tapered roller bearings, thrust roller bearings, angular contact ball bearings '
             'and wheel hub bearings. Brands stocked include NACHI, INA, Timken, NTN, Koyo, FAG, SKF and NSK.'),
            ('pneumatic-systems', 'Pneumatic Systems',
             'Pneumatic hose, fittings, quick release couplings, air hose pipes and pneumatic cylinders.',
             'We are pneumatic specialists, focused on supplying complete solutions from the generation of '
             'clean dry compressed air to industrial automation on the machine.'),
            ('pressure-gauges', 'Pressure Gauges',
             'Utility pressure gauges, stainless steel pressure gauges, vibration-proof (liquid filled) '
             'pressure gauges and low pressure capsule pressure gauges.',
             'We are committed to achieving full satisfaction from the user\u2019s end. Our in-depth knowledge '
             'in the field ensures we offer our clients a customized range of pressure gauges for complete '
             'customer satisfaction.'),
            ('industrial-tools', 'Industrial Tools',
             'Sockets, wrenches, ratchets, mallets, screwdrivers, pry bars, all kinds of pullers, and other '
             'hand tools, in a variety of sizes to fit the job.',
             'We supply industrial mechanical tools that has an assortment of sockets, wrenches, ratchets, '
             'mallets, screwdrivers, pry bars, all kind of pullers, and other hand tools, in a variety of '
             'sizes to fit the job.'),
            ('mechanical-seals', 'Mechanical Seals',
             'Mechanical seals able to withstand a wide range of media, aggregate states, and varying '
             'pressure and temperature.',
             'We supply mechanical seals that are able to withstand a wide range of media, different '
             'aggregate states and varying pressure and temperature, and provide special solutions for small '
             'installations up to seal contact areas of several meters. Every application has its own '
             'special requirements profile, and our job is to provide the best sealing solution.'),
            ('oil-seals', 'Oil Seals',
             'Single lip seals, double lip seals and spring-loaded seals — standardized to customized.',
             'An oil seal is a mechanical component used in machinery to keep lubricants inside moving parts '
             'while stopping dirt and water from getting in. We supply all kinds of oil seals, from '
             'standardized to customized.'),
            ('fasteners', 'Fasteners',
             'Mechanical hardware components used to temporarily or permanently secure two or more parts '
             'together.',
             'We supply mechanical hardware components used to temporarily or permanently secure two or '
             'more parts together.'),
            ('o-rings', 'O-Rings',
             'Over 10,000 O-ring models, in Nitrile (NBR/Buna-N), Viton (FKM), EPDM, Silicone (VMQ) and HNBR.',
             'Our O-rings have more than 10,000 models, widely used in automobile manufacturing, '
             'agricultural machinery manufacturing, motor manufacturing, reducer manufacturing, hydraulic '
             'pneumatic, steel plant, coal mine, chemical machinery and other machinery manufacturing '
             'industries. Common O-ring materials: Nitrile (NBR/Buna-N), Viton (FKM/Fluoroelastomer), EPDM, '
             'Silicone (VMQ), HNBR.'),
            ('sms-union-gaskets', 'SMS Union Gaskets',
             'Hygienic, square-profile elastomeric seals for Swedish Metric Standard (SMS) pipe unions.',
             'SMS union gaskets are hygienic, square-profile elastomeric seals used in Swedish Metric '
             'Standard (SMS) pipe unions for dairy, food, beverage, and pharmaceutical processing lines.'),
            ('cleaning-sanitary-equipment', 'Industrial Cleaning & Sanitary Equipment',
             'Heavy-duty machinery, specialized tools, and hygienic systems for factories and processing '
             'plants.',
             'Industrial cleaning and sanitary equipment includes heavy-duty machinery, specialized tools, '
             'and hygienic systems designed to maintain safety and strict cleanliness in demanding '
             'environments like factories and processing plants.'),
            ('hardware', 'Hardware',
             'General hardware, including cutting discs, steel pipes and site hardware.',
             ''),
        ]
        for i, (slug, title, short_desc, desc) in enumerate(products):
            ServiceCategory.objects.get_or_create(
                slug=slug,
                defaults=dict(kind='product', title=title, short_description=short_desc,
                              description=desc, order=i, is_featured=False),
            )

        # ---- Services we offer (from the "SERVICES" section of WEBSITEE_CONTENTS.docx) ----
        services = [
            ('engineering-workshop', 'Engineering Workshop',
             'Professional, high-quality machining, cardan shaft balancing, welding and fabrication '
             'services.',
             'We have an engineering workshop that offers professional, high-quality machining, cardan '
             'shaft balancing, welding, and fabrication services. We have an engineering partner, delivering '
             'dependable, high-precision solutions across a wide range of industries. With a fully equipped '
             'workshop and a team of skilled technicians, we are committed to excellence, fast turnaround '
             'times, and competitive pricing.'),
            ('hot-cold-insulation', 'Hot and Cold Insulation',
             'Specialized thermal barriers designed to control heat transfer, conserve energy and protect '
             'equipment.',
             'Hot and cold insulation are specialized thermal barriers designed to control heat transfer, '
             'conserve energy, and protect equipment in industrial and building systems.'),
            ('factory-audits', 'Factory Audits',
             'A systematic evaluation of a manufacturing plant, process, or quality management system.',
             'An industrial audit is a systematic evaluation of a manufacturing plant, process, or quality '
             'management system to verify compliance with standards, identify operational gaps, and drive '
             'continuous improvement. We mainly assess an external facility\u2019s production capacity, '
             'machinery condition, and reliability.'),
            ('scrap-metal-trading', 'Buying and Exporting Dry Steel and Scrap',
             'Collecting, recycling, processing and trading metals — licensed scrap metal buyer and '
             'exporter.',
             'We specialize in the industry of steel and steel scrap trading, collecting various kinds of '
             'metal scraps. We have been one of the rapidly growing companies engaged in collecting a wide '
             'range of metal scraps. We can offer our clients a wide range of services in order to make the '
             'removal of scrap both convenient and cost-efficient. With ready access to a range of vehicles, '
             'we are able to ensure fast and efficient pick-up. We are experts in the domestic and '
             'international trade. Our company ensures fast payment, regulatory compliance, and a fully '
             'responsive staff. We are dedicated to the collection, recycling, processing and trade of '
             'metals.'),
        ]
        for i, (slug, title, short_desc, desc) in enumerate(services):
            ServiceCategory.objects.get_or_create(
                slug=slug,
                defaults=dict(kind='service', title=title, short_description=short_desc,
                              description=desc, order=i, is_featured=False),
            )

        # Remove any stale ServiceCategory rows left over from an earlier
        # version of this seed (e.g. the original invented "Machine
        # Overhauling" / "Gearbox Repair" / "Reverse Engineering" list).
        # Anything whose slug isn't one of the 15 real product/service
        # slugs above gets deleted, so re-running this command always
        # leaves exactly the real list — no duplicates, no orphaned
        # fabricated entries left showing on the site.
        real_slugs = [p[0] for p in products] + [s[0] for s in services]
        stale = ServiceCategory.objects.exclude(slug__in=real_slugs)
        stale_count = stale.count()
        if stale_count:
            stale_titles = ', '.join(stale.values_list('title', flat=True))
            self.stdout.write(self.style.WARNING(
                f'Removing {stale_count} old entries not in the real list: {stale_titles}'
            ))
            stale.delete()

        # Feature a representative spread of both products and services on the homepage.
        featured_slugs = [
            'bearings', 'pneumatic-systems', 'industrial-tools',
            'engineering-workshop', 'factory-audits', 'scrap-metal-trading',
        ]
        ServiceCategory.objects.filter(slug__in=featured_slugs).update(is_featured=True)

        # Real, verifiable facts only:
        #  - 2022: BRELA incorporation date (13 June 2022) / TIN effective date (15 June 2022)
        #  - 15: the 11 products + 4 services above
        #  - 8: the bearing brands listed in the Bearings description
        #  - Licensed: BRELA Certificate of Incorporation + Ubungo Municipal Council business licence
        stats = [
            ('2022', 'Registered in Tanzania since'),
            ('15', 'Product and service lines'),
            ('8', 'Global bearing brands stocked'),
            ('Licensed', 'BRELA registered & municipal licensed'),
        ]
        for i, (value, label) in enumerate(stats):
            Stat.objects.get_or_create(label=label, defaults={'value': value, 'order': i})

        self.stdout.write(self.style.SUCCESS('Tryvis Investments real company data seeded.'))
