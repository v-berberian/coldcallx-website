"""Offline acceptance checks for the printable acquisition asset."""
import importlib.util
from io import BytesIO
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qs
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generator', ROOT / 'scripts/generate-expired-call-sheet.py')
generator = importlib.util.module_from_spec(spec); spec.loader.exec_module(generator)
data = generator.build()
assert data == generator.OUTPUT.read_bytes(), 'Committed PDF is stale'
assert data == generator.build(), 'Build is not deterministic'
reader = PdfReader(BytesIO(data))
assert len(reader.pages) == 2, 'PDF must remain two pages'
text = ' '.join(page.extract_text() for page in reader.pages)
normalize = lambda value: re.sub(r'\s+', ' ', value).strip()
for heading in generator.OPENERS + generator.OBJECTIONS:
    assert normalize(generator.source_scripts()[heading]) in normalize(text), 'Script changed or omitted: ' + heading
for label in ['Seller’s exact words', 'Agreed next step', 'Requested callback date / time']:
    assert label in text, 'Worksheet prompt missing: ' + label
links = []
for page in reader.pages:
    for ref in page.get('/Annots', []):
        annot = ref.get_object(); action = annot.get('/A', {})
        if action.get('/URI'): links.append(str(action['/URI']))
assert generator.GUIDE in links
assert generator.GUIDE + '#compliance' in links
stores = [url for url in links if urlparse(url).hostname == 'apps.apple.com']
assert len(stores) == 1
url = urlparse(stores[0]); params = parse_qs(url.query)
assert url.path.endswith('/id6751245004')
assert params['ct'] == ['blog-expired-listing-scripts']
assert params['pt'] == ['128076300'] and params['mt'] == ['8']
assert '$' not in text, 'Do not duplicate rollout pricing in this asset'
assert not reader.get_fields(), 'This offline worksheet must not collect form data'
print('PASS: deterministic two-page PDF, seven exact source excerpts, worksheet prompts, source/rules links, app ID/campaign, no duplicated prices or form fields')
