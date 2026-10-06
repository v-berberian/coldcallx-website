"""Build a printable excerpt from the reviewed HTML; never rewrite source scripts."""
from __future__ import annotations
import argparse
from html import escape
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'blog/expired-listing-scripts.html'
OUTPUT = ROOT / 'resources/expired-listing-call-sheet/expired-listing-call-sheet.pdf'
GUIDE = 'https://coldcallx.app/blog/expired-listing-scripts'
STORE = 'https://apps.apple.com/us/app/cold-call-x/id6751245004?uo=2&ct=blog-expired-listing-scripts&pt=128076300&mt=8'
OPENERS = ['1. The day-one expired opener', '3. The aged expired re-approach (30–90 days)', '4. The diagnostic call']
OBJECTIONS = ['"I\'m re-listing with my same agent."', '"We\'re taking it off the market for now."', '"What would you do differently?"', '"Your commission is too high." / "Will you cut your commission?"']

class Scripts(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.heading: list[str] | None = None
        self.script: list[str] | None = None
        self.last_heading = ''
        self.scripts: dict[str, str] = {}
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'h3': self.heading = []
        if tag == 'div' and 'script' in (dict(attrs).get('class') or '').split(): self.script = []
    def handle_data(self, data: str) -> None:
        if self.heading is not None: self.heading.append(data)
        if self.script is not None: self.script.append(data)
    def handle_endtag(self, tag: str) -> None:
        if tag == 'h3' and self.heading is not None:
            self.last_heading = ''.join(self.heading).strip(); self.heading = None
        if tag == 'div' and self.script is not None:
            self.scripts[self.last_heading] = ''.join(self.script).strip(); self.script = None

def source_scripts() -> dict[str, str]:
    parser = Scripts(); parser.feed(SOURCE.read_text())
    for key in OPENERS + OBJECTIONS:
        if key not in parser.scripts: raise ValueError('Reviewed script missing: ' + key)
    return parser.scripts

def build() -> bytes:
    scripts = source_scripts(); output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=42, leftMargin=42,
                           topMargin=42, bottomMargin=47, title='Expired Listing Call Sheet',
                           author='Cold Call X', subject='Three reviewed openers and four objection responses')
    styles = {
        'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#1d1d1f'), spaceAfter=12),
        'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=12, leading=16, spaceBefore=12, spaceAfter=6),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=14.5, spaceAfter=9, alignment=TA_LEFT),
        'small': ParagraphStyle('small', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=8, textColor=colors.HexColor('#424245')),
    }
    flow = []
    def add(text: str, style: str = 'body') -> None:
        flow.append(Paragraph(text, styles[style]))
    def response(key: str, label: str) -> None:
        add(escape(label), 'heading'); add(escape(scripts[key]))
    def link(url: str, text: str) -> str:
        return '<link href="' + escape(url, quote=True) + '" color="#0066cc">' + escape(text) + '</link>'
    add('Expired listing call sheet', 'title')
    add('Three openers to practice before your next calling session.', 'body')
    add('Use these as conversation prompts, not a teleprompter. Replace every placeholder with an accurate detail. These scripts do not establish permission to call: check the applicable rules, respect refusals and use the '+link(GUIDE+'#compliance','full guide’s calling-rules section')+'.', 'small')
    add('First 30 seconds', 'heading')
    add('Introduce yourself and your brokerage. Name the street and why you are calling. Acknowledge the other calls. Ask one question, then listen.', 'body')
    response(OPENERS[0], '1 / Day-one expired')
    response(OPENERS[1], '2 / Aged expired: 30–90 days')
    response(OPENERS[2], '3 / Diagnostic conversation')
    add('The quoted scripts are reproduced from '+link(GUIDE, 'Cold Call X’s expired-listing guide')+'. The full page includes context, more scripts and calling rules.', 'small')
    flow.append(PageBreak())
    add('Four common objections', 'title')
    add('Practice the response; do not promise anything you cannot deliver.', 'small')
    for key in OBJECTIONS: response(key, key.replace('"', ''))
    add('Record the next step', 'heading')
    for label in ['Seller’s exact words', 'Agreed next step', 'Requested callback date / time']:
        add(escape(label), 'small'); flow.append(Spacer(1, 10)); flow.append(HRFlowable(width='100%', thickness=.5, color=colors.HexColor('#b8b8bd'))); flow.append(Spacer(1, 5))
    add('Work through your own list on iPhone', 'heading')
    add('Cold Call X is a power dialer: call one lead at a time from your own cellular line, record an outcome and keep notes. '+link('https://coldcallx.app/auto-dialer-iphone','See the workflow and tradeoffs')+' or '+link(STORE,'view the App Store listing')+' for current requirements and local pricing.', 'small')
    def page_footer(c: canvas.Canvas, _: SimpleDocTemplate) -> None:
        c.saveState(); c.setFont('Helvetica', 8); c.setFillColor(colors.HexColor('#6e6e73'))
        c.drawString(42, 26, 'Cold Call X | Script excerpts from the reviewed guide | October 2026')
        c.drawRightString(570, 26, str(c.getPageNumber())); c.restoreState()
    def invariant_canvas(*args: object, **kwargs: object) -> canvas.Canvas:
        kwargs['invariant'] = 1
        return canvas.Canvas(*args, **kwargs)
    doc.build(flow, onFirstPage=page_footer, onLaterPages=page_footer, canvasmaker=invariant_canvas)
    return output.getvalue()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    data = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data: raise SystemExit('Call sheet is stale; regenerate it from reviewed source.')
        print('Call sheet matches reviewed source and generator.')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_bytes(data); print('Built ' + str(OUTPUT.relative_to(ROOT)))
