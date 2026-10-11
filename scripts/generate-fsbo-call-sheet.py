"""Build the printable FSBO call sheet from the reviewed HTML; never rewrite source scripts."""
from __future__ import annotations
import argparse
from html import escape
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'blog/fsbo-scripts.html'
OUTPUT = ROOT / 'resources/fsbo-call-sheet/fsbo-call-sheet.pdf'
GUIDE = 'https://coldcallx.app/blog/fsbo-scripts'
LANDING = 'https://coldcallx.app/resources/fsbo-call-sheet/'
PRINT_SOURCE = 'coldcallx.app/blog/fsbo-scripts'
FONT_LICENSE = ROOT / 'resources/fsbo-call-sheet/FONT_LICENSE.txt'
STORE = 'https://apps.apple.com/us/app/cold-call-x/id6751245004?uo=2&ct=resource-fsbo-call-sheet&pt=128076300&mt=8'
OPENERS = ['1. The buyer-first opener', '2. The straight-shooter', '4. The aged FSBO, 30 to 60 days in']
FOLLOW_UP = 'Day 4: the value-delivery call'
OBJECTIONS = ['"I\'m not paying a commission."', '"I\'m not interested."', '"I\'ll call you when I need an agent."', '"How did you get my number?"']

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
    for key in OPENERS + [FOLLOW_UP] + OBJECTIONS:
        if key not in parser.scripts: raise ValueError('Reviewed script missing: ' + key)
    return parser.scripts

def build() -> bytes:
    scripts = source_scripts(); output = BytesIO()
    fonts = Path(reportlab.__file__).resolve().parent / 'fonts'
    pdfmetrics.registerFont(TTFont('CCXVera', str(fonts / 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('CCXVeraBold', str(fonts / 'VeraBd.ttf')))
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=42, leftMargin=42,
                           topMargin=42, bottomMargin=47, title='FSBO Call Sheet',
                           author='Cold Call X', subject='Three reviewed FSBO openers, a day-4 follow-up and four objection responses')
    styles = {
        'title': ParagraphStyle('title', fontName='CCXVeraBold', fontSize=22, leading=26, textColor=colors.HexColor('#1d1d1f'), spaceAfter=12),
        'heading': ParagraphStyle('heading', fontName='CCXVeraBold', fontSize=12, leading=16, spaceBefore=12, spaceAfter=6),
        'body': ParagraphStyle('body', fontName='CCXVera', fontSize=10.5, leading=14.5, spaceAfter=9, alignment=TA_LEFT),
        'small': ParagraphStyle('small', fontName='CCXVera', fontSize=9, leading=12, spaceAfter=8, textColor=colors.HexColor('#424245')),
    }
    flow = []
    def add(text: str, style: str = 'body') -> None:
        flow.append(Paragraph(text, styles[style]))
    def response(key: str, label: str) -> None:
        add(escape(label), 'heading'); add(escape(scripts[key]))
    def link(url: str, text: str) -> str:
        return '<link href="' + escape(url, quote=True) + '" color="#0066cc">' + escape(text) + '</link>'
    add('FSBO call sheet', 'title')
    add('Three openers and the day-4 follow-up, to keep next to the phone.', 'body')
    add('Use these as conversation prompts, not a teleprompter. Replace every placeholder with an accurate detail, and only quote sales you have actually pulled. A posted phone number is not a Do Not Call exemption: check the '+link(GUIDE+'#legal','full guide’s calling-rules section')+', respect refusals and note who asked not to be called again.', 'small')
    add('First 10 seconds', 'heading')
    add('Say your name. Say it is a cold call about the house on their street. Say you are not calling to talk them out of selling solo. Ask for thirty seconds, then listen.', 'body')
    response(OPENERS[0], '1 / Buyer-first opener (first call)')
    response(OPENERS[1], '2 / Straight-shooter (first call)')
    response(OPENERS[2], '3 / Aged FSBO: 30 to 60 days in')
    response(FOLLOW_UP, '4 / Day 4: the value-delivery follow-up')
    add('The quoted scripts are reproduced from '+link(GUIDE, 'Cold Call X’s FSBO scripts guide')+'. The full page has six openers, the follow-up scripts, the listing-appointment ask and the calling rules.', 'small')
    add('Printed copy? Full source: ' + link(GUIDE, PRINT_SOURCE), 'small')
    flow.append(PageBreak())
    add('Four FSBO objections', 'title')
    add('Practice the response; do not promise anything you cannot deliver.', 'small')
    for key in OBJECTIONS: response(key, key.replace('"', ''))
    add('Cadence', 'heading')
    add('Day 1 opener. Day 4 deliver the promised value. Day 10 to 14 check-in. Every 7 to 10 days after that, a thirty-second call with a new reason. Week 4 to 8: the price-and-showings diagnostic and the appointment ask.', 'body')
    add('Record the next step', 'heading')
    for label in ['Seller’s exact words', 'Asking price / showings so far', 'Agreed next step and callback date / time']:
        add(escape(label), 'small'); flow.append(Spacer(1, 10)); flow.append(HRFlowable(width='100%', thickness=.5, color=colors.HexColor('#b8b8bd'))); flow.append(Spacer(1, 5))
    add('Work your FSBO list on iPhone', 'heading')
    add('Cold Call X is a power dialer: call one lead at a time from your own cellular line, tap the outcome, and the follow-up schedules itself. '+link(LANDING,'See what this sheet covers')+' or '+link(STORE,'view the App Store listing')+' for current requirements and local pricing.', 'small')
    def page_footer(c: canvas.Canvas, _: SimpleDocTemplate) -> None:
        c.saveState(); c.setFont('CCXVera', 8); c.setFillColor(colors.HexColor('#6e6e73'))
        c.drawString(42, 26, 'Cold Call X | Script excerpts from the reviewed FSBO guide | October 2026')
        c.drawRightString(570, 26, str(c.getPageNumber())); c.restoreState()
    def invariant_canvas(*args: object, **kwargs: object) -> canvas.Canvas:
        kwargs['invariant'] = 1
        kwargs['initialFontName'] = 'CCXVera'
        return canvas.Canvas(*args, **kwargs)
    doc.build(flow, onFirstPage=page_footer, onLaterPages=page_footer, canvasmaker=invariant_canvas)
    writer = PdfWriter(clone_from=PdfReader(BytesIO(output.getvalue())))
    writer.add_attachment('FONT_LICENSE.txt', FONT_LICENSE.read_bytes())
    final = BytesIO(); writer.write(final)
    return final.getvalue()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    data = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data: raise SystemExit('FSBO call sheet is stale; regenerate it from reviewed source.')
        print('FSBO call sheet matches reviewed source and generator.')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_bytes(data); print('Built ' + str(OUTPUT.relative_to(ROOT)))
