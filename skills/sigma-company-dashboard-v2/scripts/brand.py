"""SoFi brand kit. Colours are taken from the official logo asset itself
(Wikimedia Commons SoFi_logo.svg): the mark is #00A2C7 and its gradient runs
#0074F5 -> #03AAFF."""

import base64
import pathlib

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

# Defaults are SoFi; apply() rebinds them from the active company config so the
# whole build retargets from one place. Module-level names are kept (rather than
# a palette object) so none of the call sites have to change.
NAVY = "#0B2740"
NAVY_DEEP = "#06172A"
SOFI_BLUE = "#00A2C7"
SOFI_BRIGHT = "#0074F5"
SOFI_CYAN = "#03AAFF"
SOFI_MINT = "#00C4A7"
COMPANY = "SoFi"
LOGO_DOMAIN = "sofi.com"


def apply(cfg):
    """Rebind the palette to a company config. Called once at import time."""
    global NAVY, NAVY_DEEP, SOFI_BLUE, SOFI_BRIGHT, SOFI_CYAN, SOFI_MINT
    global CATEGORICAL, TEXT_DARK, COMPANY, LOGO_DOMAIN
    pal = cfg["palette"]
    NAVY, NAVY_DEEP = pal["navy"], pal["navy_deep"]
    SOFI_BRIGHT, SOFI_BLUE = pal["primary"], pal["secondary"]
    SOFI_CYAN, SOFI_MINT = pal["accent"], pal["mint"]
    TEXT_DARK = pal["navy"]
    COMPANY, LOGO_DOMAIN = cfg["name"], cfg["logo_domain"]
    global LOGO_PREFIX, LOGO_CHIP
    LOGO_PREFIX = {"mcd": "mcd"}.get(cfg["key"], cfg["key"])
    LOGO_CHIP = cfg.get("logo_chip", False)
    CATEGORICAL = [SOFI_BRIGHT, SOFI_MINT, NAVY, SOFI_CYAN,
                   SOFI_BLUE, "#7CC7E8", "#4A90E2", "#0A4E8B"]

# Light-surface system so native dark text stays high-contrast everywhere.
CANVAS = "#EEF2F7"
CARD = "#FFFFFF"
CARD_ALT = "#F4F8FC"
BORDER = "#DCE4EE"
TEXT_DARK = "#0B2740"
TEXT_MUTED = "#5B6B7F"
GOOD = "#0EA5A0"
BAD = "#EF4444"
WARN = "#E1A32D"

# All SoFi family -- the old list carried a purple (#5B4B8A) and a gold
# (#E1A32D) that read as someone else's brand in the donut and the category bars.
CATEGORICAL = [SOFI_BRIGHT, SOFI_MINT, NAVY, SOFI_CYAN,
               SOFI_BLUE, "#7CC7E8", "#4A90E2", "#0A4E8B"]


def datauri_svg(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


LOGO_PREFIX = "sofi"
LOGO_CHIP = False  # True for a multi-colour brand mark that must not be
                   # recoloured white (see the eBay/Fox News Media exception
                   # in HANDOFF.md sec 17) -- rendered on a white chip instead.


def _uri(name: str) -> str:
    """Logo data-URI for the active company, falling back to the white mark when
    a prospect only has one recolour on disk."""
    f = ASSETS / ("%s_logo_%s.datauri.txt" % (LOGO_PREFIX, name))
    if not f.exists():
        f = ASSETS / ("%s_logo_white.datauri.txt" % LOGO_PREFIX)
    return f.read_text().strip()


def logo_white():
    return _uri("white")


def logo_navy():
    return _uri("navy")


def logo_blue():
    return _uri("blue")


def logo_chip():
    return LOGO_CHIP


def logo_img_style():
    """Style for the header/modal logo image. Multi-colour marks (LOGO_CHIP)
    sit on a white chip instead of being recoloured white -- flattening a
    logo that carries its own brand colour blocks (e.g. Fox News Media's
    blue/red bands) to solid white makes the wordmark unreadable."""
    style = {"fit": "contain", "align": "start", "padding": "none"}
    if LOGO_CHIP:
        style.update({"backgroundColor": "#FFFFFF", "borderRadius": "round"})
    return style


def header_bg(width=1600, height=240) -> str:
    """Brand-gradient header band with a soft radial glow and faint rings."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="{NAVY_DEEP}"/>
      <stop offset="42%" stop-color="{NAVY}"/>
      <stop offset="100%" stop-color="{SOFI_BRIGHT}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.78" cy="0.3" r="0.6">
      <stop offset="0%" stop-color="{SOFI_CYAN}" stop-opacity="0.45"/>
      <stop offset="60%" stop-color="{SOFI_BLUE}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{NAVY}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#g)"/>
  <rect width="{width}" height="{height}" fill="url(#glow)"/>
  <g fill="none" stroke="#FFFFFF" stroke-opacity="0.07">
    <circle cx="{int(width*0.79)}" cy="{int(height*0.34)}" r="118"/>
    <circle cx="{int(width*0.79)}" cy="{int(height*0.34)}" r="184"/>
    <circle cx="{int(width*0.79)}" cy="{int(height*0.34)}" r="250"/>
  </g>
  <rect y="{height-3}" width="{width}" height="3" fill="{SOFI_CYAN}" fill-opacity="0.9"/>
</svg>"""
    return datauri_svg(svg)


def card_gradient(a=NAVY, b=SOFI_BRIGHT, width=520, height=300) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs><linearGradient id="c" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0%" stop-color="{a}"/><stop offset="100%" stop-color="{b}"/>
  </linearGradient></defs>
  <rect width="{width}" height="{height}" fill="url(#c)"/>
</svg>"""
    return datauri_svg(svg)


# card_gradient()'s gradient axis, in fractional card coordinates. Any sampler
# below has to use the SAME vector or the flat fills drift off the ramp the
# parent container paints.
_GRAD_X2, _GRAD_Y2 = 0.9, 1.0


def _mix(a: str, b: str, t: float) -> str:
    """sRGB lerp between two hexes. Good enough here -- both ends of every
    card ramp are the same hue family, so the naive blend doesn't go muddy the
    way a cross-hue lerp would."""
    a, b = a.lstrip("#"), b.lstrip("#")
    t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
    return "#" + "".join(
        "%02X" % round(int(a[i:i + 2], 16)
                       + (int(b[i:i + 2], 16) - int(a[i:i + 2], 16)) * t)
        for i in (0, 2, 4))


def gradient_sample(a, b, x0, x1, y0, y1) -> str:
    """A FLAT hex sampled off the `card_gradient(a, b)` ramp at the centre of
    the sub-rectangle (x0..x1, y0..y1), given in fractions of the card.

    Why a flat sample and not a real gradient slice: chart elements cannot
    carry a background image at all. Probed empirically against the live org
    2026-09-02, with a throwaway workbook rendered to PNG (a `create` 200 is
    not evidence -- see HANDOFF.md sec 6):

      * `line-chart` + top-level `backgroundImage` -> create REJECTED,
        `Invalid kind: "line-chart"` (the misleading unrecognised-field error)
      * `kpi-chart`  + top-level `backgroundImage` -> create SUCCEEDS and the
        tile renders OPAQUE WHITE. Accepted by the validator, painted by
        nothing -- a fifth silent layout failure
      * `style.backgroundImage` on either kind -> same: accepted, renders white
      * 8-digit alpha hex (`#0B274040`, `#FFFFFF00`) as `style.backgroundColor`
        -> create REJECTED, `Invalid kind: "kpi-chart"`. So a chart cannot be
        made even partly see-through, and the parent container's gradient can
        never show through one.

    A chart's only working background is a solid `style.backgroundColor` hex.
    Sampling that hex per child off one shared ramp is what makes a card read
    as a continuous gradient instead of flat colour blocks.
    """
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    # scalar projection of the centre onto the gradient axis, normalised
    t = (cx * _GRAD_X2 + cy * _GRAD_Y2) / (_GRAD_X2 ** 2 + _GRAD_Y2 ** 2)
    return _mix(a, b, t)


# ---------------------------------------------------------------------------
# ONE ramp across the whole KPI row
#
# card_gradient/gradient_sample above ramp within a SINGLE card, so a four-card
# row reads as four separate gradients. The helpers below instead treat the
# entire row as one coordinate space -- x runs 0..1 across ALL the cards, y
# runs 0..1 down one card -- so each card renders its own slice of a single
# continuous ramp and the row reads as one sweep left to right.
#
# The axis is deliberately much flatter than the per-card one: over a row four
# cards wide, card_gradient's near-45' vector would resolve almost entirely
# into the vertical, and the left-to-right sweep would be invisible. Keeping a
# small vertical component stops it looking like a flat horizontal wipe.
_ROW_GRAD_X2, _ROW_GRAD_Y2 = 1.0, 0.25


def _row_t(x: float, y: float) -> float:
    """Position along the row ramp (0..1) for a point in row-global space."""
    t = (x * _ROW_GRAD_X2 + y * _ROW_GRAD_Y2) / (_ROW_GRAD_X2 ** 2 + _ROW_GRAD_Y2 ** 2)
    return 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)


def row_gradient_sample(a, b, x0, x1, y0, y1) -> str:
    """Flat hex off the ROW-wide ramp at the centre of a row-global sub-rect.

    Same hard constraint as gradient_sample() -- see its docstring for the
    probe -- a chart element can only ever paint a solid backgroundColor, so
    each tile gets the single colour the row ramp has at its own position.
    """
    return _mix(a, b, _row_t((x0 + x1) / 2.0, (y0 + y1) / 2.0))


# How far along a->b the row ramp is allowed to travel. Every KPI tile carries
# WHITE text (value, label, and the delta badge), so the bright end has to stay
# dark enough to hold it. Running the ramp all the way to SOFI_BRIGHT puts the
# last card at ~3.3:1 -- below WCAG AA's 4.5:1 for the 12-13px labels, and
# worse than the per-card ramp this replaced. 0.80 is the furthest that still
# clears 4.5:1 on Emburse's #0097DC; re-check with a darker brand primary if a
# company ever looks washed out here.
ROW_RAMP_MAX_T = 0.80


def row_ramp_ends(a, b):
    """(dark, bright) endpoints for the KPI row ramp, bright end capped to
    ROW_RAMP_MAX_T so white text stays legible on the last card."""
    return a, _mix(a, b, ROW_RAMP_MAX_T)


def row_gradient_slice(a, b, x0, x1, width=520, height=300) -> str:
    """SVG data URI for ONE card's container background: the x0..x1 horizontal
    slice of the row-wide ramp. Containers (unlike charts) do take a real
    background image, so this is what keeps the gutters and the rounded corners
    between cards continuous with the ramp instead of stepping at each card."""
    ca = _mix(a, b, _row_t(x0, 0.0))
    cb = _mix(a, b, _row_t(x1, 1.0))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs><linearGradient id="c" x1="0" y1="0" x2="1" y2="{_ROW_GRAD_Y2}">
    <stop offset="0%" stop-color="{ca}"/><stop offset="100%" stop-color="{cb}"/>
  </linearGradient></defs>
  <rect width="{width}" height="{height}" fill="url(#c)"/>
</svg>"""
    return datauri_svg(svg)


def icon(path_d: str, color=SOFI_BRIGHT, size=24) -> str:
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
           f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
           f'stroke-linecap="round" stroke-linejoin="round">{path_d}</svg>')
    return datauri_svg(svg)


ICON_SPARK = '<polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
ICON_TREND = ('<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
              '<polyline points="17 6 23 6 23 12"/>')
ICON_USERS = ('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
              '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>')
ICON_WHEEL = ('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/>'
              '<line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/>'
              '<line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/>')
ICON_SLIDERS = ('<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/>'
                '<line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/>'
                '<line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/>'
                '<line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/>'
                '<line x1="17" y1="16" x2="23" y2="16"/>')
