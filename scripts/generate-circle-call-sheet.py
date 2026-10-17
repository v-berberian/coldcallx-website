"""Build the printable circle prospecting call sheet from the reviewed HTML; never rewrite source scripts."""
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
SOURCE = ROOT / 'blog/circle-prospecting-scripts.html'
OUTPUT = ROOT / 'resources/circle-prospecting-call-sheet/circle-prospecting-call-sheet.pdf'
GUIDE = 'https://coldcallx.app/blog/circle-prospecting-scripts'
LANDING = 'https://coldcallx.app/resources/circle-prospecting-call-sheet/'
PRINT_SOURCE = 'coldcallx.app/blog/circle-prospecting-scripts'
FONT_LICENSE = ROOT / 'resources/circle-prospecting-call-sheet/FONT_LICENSE.txt'
STORE = 'https://apps.apple.com/us/app/cold-call-x/id6751245004?uo=2&ct=resource-circle-call-sheet&pt=128076300&mt=8'
OPENERS = ['1. Just-listed script', '2. Open-house invitation', '3. Under-contract script', '4. Just-sold script']
MARKET_UPDATE = 'Between listings? The market-update circle'
OBJECTIONS = ['“We’re not moving.”', '“How did you get my number?”', '“Just send me something.”', '“Take me off your list.”']
WORKSHEET = ['Anchor property, event and date', 'Ring size, list source and Do Not Call scrub date', 'Homeowner’s exact words', 'Agreed next step and callback date / time']

class Scripts(HTMLParser):
    """Map each script block to the nearest preceding h2 or h3 heading."""
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.heading: list[str] | None = None
        self.script: list[str] | None = None
        self.last_heading = ''
        self.scripts: dict[str, str] = {}
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ('h2', 'h3'): self.heading = []
        if tag == 'div' and 'script' in (dict(attrs).get('class') or '').split(): self.script = []
    def handle_data(self, data: str) -> None:
        if self.heading is not None: self.heading.append(data)
        if self.script is not None: self.script.append(data)
    def handle_endtag(self, tag: str) -> None:
        if tag in ('h2', 'h3') and self.heading is not None:
            self.last_heading = ''.join(self.heading).strip(); self.heading = None
        if tag == 'div' and self.script is not None:
            self.scripts[self.last_heading] = ''.join(self.script).strip(); self.script = None

def source_scripts() -> dict[str, str]:
    parser = Scripts(); parser.feed(SOURCE.read_text())
    for key in OPENERS + [MARKET_UPDATE] + OBJECTIONS:
        if key not in parser.scripts: raise ValueError('Reviewed script missing: ' + key)
    return parser.scripts

def build() -> bytes:
    scripts = source_scripts(); output = BytesIO()
    fonts = Path(reportlab.__file__).resolve().parent / 'fonts'
    pdfmetrics.registerFont(TTFont('CCXVera', str(fonts / 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('CCXVeraBold', str(fonts / 'VeraBd.ttf')))
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=42, leftMargin=42,
                           topMargin=42, bottomMargin=47, title='Circle Prospecting Call Sheet',
                           author='Cold Call X', subject='Five reviewed circle prospecting scripts, four objection responses and the listing-to-closing cadence')
    styles = {
        'title': ParagraphStyle('title', fontName='CCXVeraBold', fontSize=22, leading=26, textColor=colors.HexColor('#1d1d1f'), spaceAfter=10),
        'heading': ParagraphStyle('heading', fontName='CCXVeraBold', fontSize=12, leading=16, spaceBefore=9, spaceAfter=5),
        'body': ParagraphStyle('body', fontName='CCXVera', fontSize=10.5, leading=14.5, spaceAfter=7, alignment=TA_LEFT),
        'small': ParagraphStyle('small', fontName='CCXVera', fontSize=9, leading=12, spaceAfter=7, textColor=colors.HexColor('#424245')),
    }
    flow = []
    def add(text: str, style: str = 'body') -> None:
        flow.append(Paragraph(text, styles[style]))
    def response(key: str, label: str) -> None:
        add(escape(label), 'heading'); add(escape(scripts[key]))
    def link(url: str, text: str) -> str:
        return '<link href="' + escape(url, quote=True) + '" color="#0066cc">' + escape(text) + '</link>'
    add('Circle prospecting call sheet', 'title')
    add('One script per market event on the anchor property, to keep next to the phone.', 'body')
    add('Use these as conversation prompts, not a teleprompter. Replace every placeholder with a true detail, and only quote sales and statistics you pulled yourself. A nearby listing is a reason to call, not a Do Not Call exemption: check the '+link(GUIDE+'#legal','full guide’s calling-rules section')+', respect refusals and note who asked not to be called again.', 'small')
    add('First 10 seconds', 'heading')
    add('Answer three questions: who you are, why this street, and what is in it for the homeowner. Use one trigger, lead with the address and the event, ask one question, then stop talking.', 'body')
    response(OPENERS[0], '1 / Just listed')
    response(OPENERS[1], '2 / Open-house invitation')
    response(OPENERS[2], '3 / Under contract')
    response(OPENERS[3], '4 / Just sold')
    response(MARKET_UPDATE, '5 / Between listings: the market update')
    add('The quoted scripts are reproduced from '+link(GUIDE, 'Cold Call X’s circle prospecting guide')+', which also covers where to get circle lists and the calling rules. Printed copy? Full source: ' + link(GUIDE, PRINT_SOURCE), 'small')
    flow.append(PageBreak())
    add('Four circle call objections', 'title')
    add('Keep it human; a clean no is better than a fake lead.', 'small')
    for key in OBJECTIONS: response(key, key.strip('“”'))
    add('Work one listing four times', 'heading')
    add('Week 1, just listed: the introduction call. Open house week: the personal invitation. Under contract: the buyers-are-waiting update. After closing: the just-sold value conversation. Every call needs its own real reason, and anyone who opts out comes off the list permanently.', 'body')
    add('Log the ring', 'heading')
    for label in WORKSHEET:
        add(escape(label), 'small'); flow.append(Spacer(1, 10)); flow.append(HRFlowable(width='100%', thickness=.5, color=colors.HexColor('#b8b8bd'))); flow.append(Spacer(1, 5))
    add('Work the ring on iPhone', 'heading')
    add('Cold Call X is a power dialer: import the ring from a spreadsheet, call one homeowner at a time from your own cellular line, tap the outcome, and the follow-up schedules itself. '+link(LANDING,'See what this sheet covers')+' or '+link(STORE,'view the App Store listing')+' for current requirements and local pricing.', 'small')
    def page_footer(c: canvas.Canvas, _: SimpleDocTemplate) -> None:
        c.saveState(); c.setFont('CCXVera', 8); c.setFillColor(colors.HexColor('#6e6e73'))
        c.drawString(42, 26, 'Cold Call X | Script excerpts from the reviewed circle prospecting guide | October 2026')
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
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data: raise SystemExit('Circle prospecting call sheet is stale; regenerate it from reviewed source.')
        print('Circle prospecting call sheet matches reviewed source and generator.')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_bytes(data); print('Built ' + str(OUTPUT.relative_to(ROOT)))
