"""Offline acceptance checks for the printable FSBO call sheet."""
import importlib.util
from io import BytesIO
from pathlib import Path
import re
from urllib.parse import urlparse, parse_qs
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generator', ROOT / 'scripts/generate-fsbo-call-sheet.py')
generator = importlib.util.module_from_spec(spec); spec.loader.exec_module(generator)
data = generator.build()
assert data == generator.OUTPUT.read_bytes(), 'Committed PDF is stale'
assert data == generator.build(), 'Build is not deterministic'
reader = PdfReader(BytesIO(data))
assert len(reader.pages) == 2, 'PDF must remain two pages'
assert reader.attachments['FONT_LICENSE.txt'] == [generator.FONT_LICENSE.read_bytes()], 'Embedded font license missing'
for page in reader.pages:
    for ref in page['/Resources']['/Font'].values():
        font = ref.get_object(); descriptor = font['/FontDescriptor'].get_object()
        assert descriptor.get('/FontFile2'), 'PDF text font is not embedded'
text = ' '.join(page.extract_text() for page in reader.pages)
assert generator.PRINT_SOURCE in text, 'Paper-readable source URL missing'
normalize = lambda value: re.sub(r'\s+', ' ', value).strip()
for heading in generator.OPENERS + [generator.FOLLOW_UP] + generator.OBJECTIONS:
    assert normalize(generator.source_scripts()[heading]) in normalize(text), 'Script changed or omitted: ' + heading
for label in ['Seller’s exact words', 'Asking price / showings so far', 'Agreed next step and callback date / time']:
    assert label in text, 'Worksheet prompt missing: ' + label
links = []
for page in reader.pages:
    for ref in page.get('/Annots', []):
        annot = ref.get_object(); action = annot.get('/A', {})
        if action.get('/URI'): links.append(str(action['/URI']))
assert generator.GUIDE in links
assert generator.GUIDE + '#legal' in links
assert generator.LANDING in links
stores = [url for url in links if urlparse(url).hostname == 'apps.apple.com']
assert len(stores) == 1
url = urlparse(stores[0]); params = parse_qs(url.query)
assert url.path.endswith('/id6751245004')
assert params['ct'] == ['resource-fsbo-call-sheet']
for banned in ['auto dialer', 'autodialer', 'iOS 17', '$']:
    assert banned not in text, 'Copy rule hit in PDF: ' + banned
print('FSBO call sheet checks passed.')
