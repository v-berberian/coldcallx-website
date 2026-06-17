#!/usr/bin/env python3
"""Submit the sitemap to Google Search Console via the Search Console API.

Auth uses a service-account JSON key supplied in the GSC_SA_KEY env var
(a GitHub Actions secret). If the secret is absent the script exits 0 so the
workflow stays green until setup is finished.
"""
import json
import os
import sys
import urllib.parse

sa_key = os.environ.get("GSC_SA_KEY", "").strip()
site_url = os.environ.get("GSC_SITE_URL", "sc-domain:coldcallx.app").strip()
sitemap_url = os.environ.get("SITEMAP_URL", "https://coldcallx.app/sitemap.xml").strip()

if not sa_key:
    print("GSC_SA_KEY secret is not set yet — skipping sitemap submission.")
    print("Add the service-account JSON as a repo secret named GSC_SA_KEY to enable this.")
    sys.exit(0)

try:
    info = json.loads(sa_key)
except json.JSONDecodeError as exc:
    print(f"::error::GSC_SA_KEY is not valid JSON: {exc}")
    sys.exit(1)

# Imported after the empty-secret check so local linting doesn't require the deps.
from google.oauth2 import service_account  # noqa: E402
import google.auth.transport.requests  # noqa: E402
import requests  # noqa: E402

credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/webmasters"]
)
credentials.refresh(google.auth.transport.requests.Request())

endpoint = "https://www.googleapis.com/webmasters/v3/sites/{}/sitemaps/{}".format(
    urllib.parse.quote(site_url, safe=""),
    urllib.parse.quote(sitemap_url, safe=""),
)

response = requests.put(
    endpoint,
    headers={"Authorization": f"Bearer {credentials.token}"},
    timeout=30,
)

if response.status_code in (200, 204):
    print(f"✓ Submitted {sitemap_url} to {site_url}")
    sys.exit(0)

print(f"::error::Sitemap submission failed: HTTP {response.status_code}")
print(response.text)
sys.exit(1)
