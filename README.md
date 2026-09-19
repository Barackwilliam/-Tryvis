# Tryvis Investments Limited — Website

Django site for Tryvis Investments Limited (industrial engineering & supply,
Dar es Salaam). Database: Supabase Postgres. Media (logo, gallery, partner
logos): Supabase Storage bucket via its S3-compatible API.

## 1. Local setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your real values
python manage.py migrate
python manage.py seed_company     # loads company profile, phones, services
python manage.py createsuperuser  # for /admin/
python manage.py runserver
```

## 2. Supabase setup

**Database** — Supabase dashboard → Settings → Database → copy the
"Connection pooling" values into `DB_HOST` / `DB_USER` / `DB_PASSWORD` in `.env`.

**Storage bucket** — Settings → Storage → create a bucket (e.g. `tryvis-media`),
make it Public, then go to Storage → S3 Connection to get the access key,
secret key and endpoint URL for `.env`.

## 2b. If uploaded images don't show up on the site

Run this any time — locally or on Render, via its Shell tab:

```bash
python manage.py check_storage
```

It uploads a real test file, asks Django for the URL it generated, and
fetches that URL to see what actually comes back. Read the last line:

- **`Fetch OK -> HTTP 200`** — storage is working. If an image still looks
  missing, the field is probably empty in the admin, not a storage problem.
- **`Fetch FAILED -> HTTP 403`** — the bucket is set to **Private**. Fix:
  Supabase dashboard → Storage → your bucket → Settings → make it **Public**.
  This is the single most common cause.
- **`Fetch FAILED -> HTTP 404`** — `SUPABASE_BUCKET_NAME` in your env
  doesn't match the bucket's real name (check for a typo, capital letter,
  or extra space — Supabase bucket names are case-sensitive).
- **`Upload FAILED`** — `SUPABASE_S3_ACCESS_KEY` / `SUPABASE_S3_SECRET_KEY`
  are wrong, or `SUPABASE_S3_REGION` doesn't match the project's real
  region (check the region in your `DATABASE_URL` pooler hostname, e.g.
  `aws-0-eu-west-1.pooler...` means the region is `eu-west-1`, not
  whatever `.env.example` happens to say).

Two things worth knowing about this setup, so a future change doesn't
reintroduce the bug this command catches:

- Django's `MEDIA_URL` setting is **not** what controls the link to an
  uploaded file — `storages.backends.s3.S3Storage` builds its own URL from
  `AWS_S3_CUSTOM_DOMAIN`. `settings.py` derives that automatically from
  `SUPABASE_S3_ENDPOINT`, so nothing extra needs to be set in `.env` — but
  if someone hand-edits the URL logic in `settings.py`, that's the part to
  get right.
- Supabase's S3 API path (`/storage/v1/s3`, used only for the upload
  itself) and its public file path (`/storage/v1/object/public/<bucket>`,
  used for the `<img src>` link) are two different URLs on the same
  project. Mixing them up looks exactly like "the image didn't save" —
  the upload actually succeeded, the link to view it was just wrong.

## 3. Seed content

```bash
python manage.py seed_all
```

Fills the site with the **client's real content** — nothing invented.
Company profile, phone numbers, and the full 15-item product/service list
come from the client's own `about_company.docx` and `WEBSITEE_CONTENTS.docx`
(see `seed_company.py` for exact wording). Product/service icon photos,
8 bearing-brand logos, 4 gallery photos and 3 hero slides all come from
`core/seed_assets/` — real photos and brand logos the client supplied in
their own document, extracted once and resized for the web. None of it is
stock photography or AI-generated placeholder art.

**Partner is never touched by this command** — the client manages that
list themselves in `/admin/`.

Two facts noted in `seed_company.py` are worth knowing before you seed:
- The **Values** statement ("We listen, we care, and we continue to
  uphold.") is reproduced exactly as it appears in the client's document —
  it reads as unfinished. Ask the client for the rest of the sentence
  rather than guessing an ending.
- The seeded **email** (`tryvisinvesment@gmail.com`) is spelled exactly as
  in the client's document — missing the "t" in "investment". This may be
  a typo in the underlying Gmail account itself, so it was kept verbatim
  rather than "corrected" to an address that might not exist. Confirm with
  the client before changing it.

Safe to re-run any time — it skips anything that already exists. To wipe
and regenerate just the brand logos/gallery/hero slides/icons (company
profile and the product/service text are never deleted by this command):

```bash
python manage.py seed_all --force
```

(`seed_company` alone still works too, if you only want the text content
without touching any images.)

## 3b. Adding content via /admin/

- **Company Info** → upload the logo, edit About/Vision/Mission/Values, and
  add every phone number in the inline "Phone numbers" list. The WhatsApp
  number (digits with country code, e.g. `255767644317`) switches on the
  floating WhatsApp button.
- **Hero slides** → the cross-fading background images behind the homepage
  headline. Upload landscape photos, 1920x1080 or wider. Leave this empty and
  the site falls back to three built-in engineering artworks, so the slider
  always looks finished.
- **Stats** → the four proof figures in the dark band (value + label).
- **Service categories** → the six services on the homepage; edit or add more.
- **Gallery images** → workshop / fabrication / overhaul photos.
- **Partners** → the client/partner logos shown in the trust strip.
- **Contact messages** → submissions from the site's contact form.

## 4. Run locally

```bash
python manage.py runserver
```

## 5. Deploying (Render)

This repo includes `build.sh` and `Procfile` for Render:
- Build command: `./build.sh`
- Start command: `gunicorn config.wsgi`
- Add all `.env.example` variables as Render environment variables.

**Python version**: a `.python-version` file pins the build to Python 3.12.
Without it, Render uses whatever the newest available Python is at the time
your service was created — a brand-new Python release can ship before
Django has added official support for it, which is exactly what happened
here: Render built this service on Python 3.14, and Django 5.1 doesn't
support 3.14 yet. That mismatch breaks an internal trick Django's template
engine uses (`copy()` on a `super()` object in `django/template/context.py`),
which is what threw `'super' object has no attribute 'dicts'` on the
`/admin/` pages that use a changelist (e.g. Hero slides). It isn't a bug in
this project's code — it's a Python/Django version mismatch.

If you see that error again after adding `.python-version`, the fix hasn't
taken effect yet because Render cached the old build environment. On the
Render dashboard: **Manual Deploy → Clear build cache & deploy**. A normal
deploy without clearing the cache may keep using the old Python install.

## Design

Identity: **Navy + Electric Blue + White** — a corporate system where blue is
a signal (actions, active state, emphasis) rather than a surface. White and
near-white carry the content; navy carries the header, hero, stats band, CTA
panel and footer.

| Token | Value | Use |
|---|---|---|
| `--navy` | `#0F172A` | header, footer, stats band, CTA panel |
| `--blue` | `#2563EB` | primary buttons, links, active marks |
| `--blue-hover` | `#1D4ED8` | primary button hover |
| `--sky` | `#38BDF8` | accents on navy only (never on white) |
| `--bg` | `#F8FAFC` | default page background |
| `--surface` | `#FFFFFF` | cards, panels, forms |
| `--surface-2` | `#F1F5F9` | alternating section tone |
| `--text` | `#1E293B` | body copy |
| `--text-2` | `#475569` | secondary copy |

Derived shades (`--navy-deep`, `--border`, `--border-2`, `--text-3`,
`--blue-wash`) are sampled off the same navy hue — no other colour family is
introduced. Sky blue is used only on navy backgrounds so contrast stays high.

Also defined at the top of `static/core/css/style.css`: a spacing scale
(`--s-1` … `--s-9`), three elevation levels (`--sh-xs` … `--sh-lg`, all
navy-tinted) and one radius scale (`--r-sm` `--r` `--r-lg`). Change a token
there and it propagates across every page.

Type: **Archivo** for headings, **IBM Plex Sans** for body, with a fixed
hierarchy — hero display, h1 page title, h2 section title, h3 card title,
`.lede` supporting paragraph, `.label` eyebrow.

### Notable front-end behaviour

- **Hero slider** — cross-fades `HeroSlide` images (or the three built-in SVG
  artworks in `static/core/img/`) with a slow Ken Burns zoom. Pauses when the
  tab is hidden and when the visitor prefers reduced motion.
- **Left drawer navigation** — on screens under 1080px the menu slides in from
  the left. GPU `translate3d` only, closes on Esc, on scrim tap, and on a
  left swipe.
- **Performance** — one stylesheet, ~3KB of inline JavaScript (no extra
  request), fonts preloaded without blocking render, lazy images, one-shot
  IntersectionObserver reveals. The fallback hero artworks are hand-built SVG,
  around 10KB each.
- **Footer credit** — "Designed and built by JamiiTek" links to
  <https://www.jamiitek.com>.
