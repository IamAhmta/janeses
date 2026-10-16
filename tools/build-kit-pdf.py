#!/usr/bin/env python3
"""Builds downloads/janeses-event-planning-kit.pdf  (the website's lead magnet).
Run from the project root:  python tools/build-kit-pdf.py      (needs: pip install reportlab pillow)
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
import os

NAVY, ROYAL, GOLD = HexColor("#0B3A22"), HexColor("#1D7A3B"), HexColor("#B5DB12")
GOLD_D, SLATE, TINT, LINE = HexColor("#4B7A00"), HexColor("#5C6B60"), HexColor("#F6F8F2"), HexColor("#DDE5D6")
W, H = A4
M = 46  # page margin
OUT = "downloads/janeses-event-planning-kit.pdf"
os.makedirs("downloads", exist_ok=True)
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("The Janeses Event Planning Starter Kit")
c.setAuthor("Janeses Integrated Services Ltd")

body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.4, textColor=HexColor("#2F3F34"))
small = ParagraphStyle("s", parent=body, fontSize=8.4, leading=11.6, textColor=SLATE)
white_p = ParagraphStyle("w", parent=body, textColor=HexColor("#D2E1D6"), fontSize=10.5, leading=15)

def para(text, style, x, y_top, width):
    p = Paragraph(text, style)
    w, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return h

def arch(cx, base_y, w, h, color, lw=2, fill=False):
    """Signature arch outline: straight sides + semicircular top."""
    r = w / 2
    path = c.beginPath()
    path.moveTo(cx - r, base_y)
    path.lineTo(cx - r, base_y + h - r)
    path.arcTo(cx - r, base_y + h - 2 * r, cx + r, base_y + h, 180, -180)
    path.lineTo(cx + r, base_y)
    c.setStrokeColor(color); c.setLineWidth(lw)
    if fill:
        c.setFillColor(color); c.drawPath(path, stroke=0, fill=1)
    else:
        c.drawPath(path, stroke=1, fill=0)

def page_chrome(n, eyebrow, title):
    c.setFillColor(white); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(NAVY); c.rect(0, H - 92, W, 92, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(M, H - 92, 54, 3, stroke=0, fill=1)
    c.setFont("Times-Italic", 12); c.setFillColor(GOLD)
    c.drawString(M, H - 38, eyebrow)
    c.setFont("Helvetica-Bold", 22); c.setFillColor(white)
    c.drawString(M, H - 68, title)
    c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(M, 40, W - M, 40)
    c.setFont("Helvetica", 7.8); c.setFillColor(SLATE)
    c.drawString(M, 27, "Janeses Integrated Services Ltd  |  +234 803 889 3499  |  janesesconcept@gmail.com")
    c.drawRightString(W - M, 27, f"{n}")

# ---------------------------------------------------------------- PAGE 1: cover
c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
arch(W / 2, 330, 330, 420, HexColor("#124A2C"), fill=True)
arch(W / 2, 330, 330, 420, GOLD, lw=2.4)
arch(W / 2, 342, 306, 396, HexColor("#B5DB12"), lw=0.6)
from PIL import Image, ImageDraw
_im = Image.open("images/logo-mark-375.webp").convert("RGBA")
_s = min(_im.size); _im = _im.crop((0, 0, _s, _s))
_m = Image.new("L", (_s * 3, _s * 3), 0); ImageDraw.Draw(_m).ellipse((6, 6, _s * 3 - 6, _s * 3 - 6), fill=255)
_im.putalpha(_m.resize((_s, _s), Image.LANCZOS))
c.drawImage(ImageReader(_im), W / 2 - 52, 642, 104, 104, mask="auto")
c.setFont("Times-Italic", 15); c.setFillColor(GOLD)
c.drawCentredString(W / 2, 600, "A free guide from Janeses")
c.setFillColor(white); c.setFont("Helvetica-Bold", 31)
c.drawCentredString(W / 2, 548, "The Event Planning")
c.drawCentredString(W / 2, 508, "Starter Kit")
c.setFont("Helvetica", 11); c.setFillColor(HexColor("#D2E1D6"))
for i, t in enumerate(["A 12-week countdown checklist, a budget planner",
                       "and a day-of timeline for weddings, birthdays",
                       "and corporate events."]):
    c.drawCentredString(W / 2, 462 - i * 16, t)
c.setFillColor(GOLD); c.rect(W / 2 - 27, 392, 54, 3, stroke=0, fill=1)
c.setFont("Helvetica-Bold", 10.5); c.setFillColor(white)
c.drawCentredString(W / 2, 355, "JANESES INTEGRATED SERVICES LTD")
c.setFont("Times-Italic", 11); c.setFillColor(HexColor("#9DB5A3"))
c.drawCentredString(W / 2, 338, "Your One-Stop Shop for Premium Services")
c.setFont("Helvetica", 9); c.setFillColor(HexColor("#9DB5A3"))
c.drawCentredString(W / 2, 60, "Sunny Peace Plaza, Zaria Road, Jos, Plateau State, Nigeria")
c.showPage()

# ---------------------------------------------------------------- PAGE 2: 12-week countdown
page_chrome(2, "Step 1", "Your 12-week countdown")
y = H - 120
y -= para("Tick each box as you go. Shorter runway? Compress the timeline, but keep the order: "
          "<b>date, budget and venue first</b>, then the vendors that book up fastest "
          "(catering, decor, cake), then the details.", body, M, y, W - 2 * M) + 14

stages = [
    ("12+ weeks out", "Lock the foundations", [
        "Set your date and a realistic guest estimate",
        "Agree your total budget and who is paying for what",
        "Name one person as the final decision-maker",
        "Shortlist and book your venue",
        "Start the guest list (family, friends, VIPs)"]),
    ("8 to 12 weeks", "Book the big vendors", [
        "Book caterer, decorator and cake designer",
        "Choose your theme and colour palette",
        "Brides: choose attire and book makeup / parlor session",
        "Book photo and video; arrange sound and MC"]),
    ("4 to 8 weeks", "Shape the experience", [
        "Hold a menu tasting and a cake flavour tasting",
        "Approve the decor concept and venue floor plan",
        "Send invitations and open RSVPs",
        "Plan drinks and confirm rentals (tables, chairs, linen)"]),
    ("2 to 4 weeks", "Put it in writing", [
        "Finalise guest count and seating plan",
        "Get every vendor's arrival time and scope in writing",
        "Schedule final payments and keep receipts together"]),
    ("Final week", "Prepare to enjoy it", [
        "Reconfirm delivery and setup times with each vendor",
        "Pack an emergency kit (pins, tape, chargers, first aid)",
        "Share the day-of timeline with your core team"]),
]
col_w = W - 2 * M - 112
for label, sub, items in stages:
    # compute block height
    ph = [Paragraph(t, body) for t in items]
    hs = [p.wrap(col_w - 24, 500)[1] for p in ph]
    block_h = sum(h + 5 for h in hs) + 8
    c.setFillColor(TINT); c.roundRect(M, y - block_h, W - 2 * M, block_h, 8, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(M, y - block_h, 3.2, block_h, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 10.2); c.setFillColor(NAVY); c.drawString(M + 14, y - 17, label)
    c.setFont("Times-Italic", 10); c.setFillColor(GOLD_D); c.drawString(M + 14, y - 31, sub)
    yy = y - 8
    for p, h in zip(ph, hs):
        c.setStrokeColor(GOLD_D); c.setLineWidth(1); c.roundRect(M + 112, yy - 11, 9, 9, 2, stroke=1, fill=0)
        p.drawOn(c, M + 112 + 20, yy - h)
        yy -= h + 5
    y -= block_h + 10
# tip callout
c.setFillColor(HexColor("#F2F9CC")); c.roundRect(M, y - 54, W - 2 * M, 54, 8, stroke=0, fill=1)
c.setFont("Helvetica-Bold", 9.6); c.setFillColor(GOLD_D); c.drawString(M + 14, y - 20, "PLANNING TIP")
para("Popular dates and festive-season weekends fill up first. Secure your venue, caterer and decorator "
     "before you spend time on smaller details.", body, M + 14, y - 26, W - 2 * M - 28)
c.showPage()

# ---------------------------------------------------------------- PAGE 3: budget planner
page_chrome(3, "Step 2", "Your budget planner")
y = H - 120
y -= para("Use the middle column as a <b>starting point</b>, not a rule. Every event is different: a "
          "wedding leans on attire and decor, a corporate dinner on catering and venue. Fill in your "
          "total first, then split it, and <b>set aside a contingency before anything else</b>.",
          body, M, y, W - 2 * M) + 16

c.setFont("Helvetica-Bold", 10); c.setFillColor(NAVY)
c.drawString(M, y - 4, "My total budget:  NGN"); c.setStrokeColor(SLATE); c.setLineWidth(0.7)
c.line(M + 118, y - 6, M + 260, y - 6)
y -= 24

rows = [["Category", "Typical share", "My budget (NGN)", "Actual (NGN)"],
        ["Venue and rentals", "15 - 20%", "", ""],
        ["Catering and drinks", "30 - 40%", "", ""],
        ["Decor and styling", "10 - 18%", "", ""],
        ["Cake and desserts", "3 - 6%", "", ""],
        ["Attire, bridal and beauty", "8 - 12%", "", ""],
        ["Photo, video and entertainment", "8 - 10%", "", ""],
        ["Logistics and miscellaneous", "4 - 8%", "", ""],
        ["Contingency (keep this untouched)", "8 - 10%", "", ""],
        ["TOTAL", "", "", ""]]
t = Table(rows, colWidths=[196, 82, 108, 108], rowHeights=[26] + [28] * 9)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 1), (-1, -1), 9.4),
    ("TEXTCOLOR", (0, 1), (-1, -1), HexColor("#2F3F34")),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"), ("BACKGROUND", (0, -1), (-1, -1), HexColor("#F2F9CC")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -2), [white, TINT]),
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("ALIGN", (1, 0), (1, -1), "CENTER"),
]))
tw, th = t.wrap(W, H)
t.drawOn(c, M, y - th)
y -= th + 24

c.setFont("Helvetica-Bold", 11); c.setFillColor(NAVY); c.drawString(M, y, "Five habits that protect your budget")
y -= 10
tips = [
    "<b>Guest count drives everything.</b> Catering, drinks, seating and rentals all scale with it, so settle a number early and revisit it only with a reason.",
    "<b>Ask for itemised quotes.</b> You can only compare vendors fairly when each line (food, service staff, setup, delivery) is visible.",
    "<b>Put every agreement in writing</b>, including what is and is not included, payment dates and the cancellation terms.",
    "<b>Spend where guests will notice.</b> Food, comfort and one memorable focal point (a backdrop, an entrance, a cake) beat small touches everywhere.",
    "<b>Track as you pay.</b> Use the Actual column every time a deposit or balance goes out, so there are no surprises in the final week.",
]
for i, tp in enumerate(tips):
    y -= 8
    c.setFillColor(GOLD); c.circle(M + 4, y - 7, 3, stroke=0, fill=1)
    y -= para(tp, body, M + 16, y, W - 2 * M - 16)
c.showPage()

# ---------------------------------------------------------------- PAGE 4: day-of timeline + vendor questions + CTA
page_chrome(4, "Step 3", "Day-of timeline and vendor questions")
y = H - 120
y -= para("Fill this in with your team a week before the event and share it with every vendor. "
          "The example rows show the level of detail that keeps a day calm.", body, M, y, W - 2 * M) + 12
rows = [["Time", "What happens", "Who is responsible"],
        ["7:00 am", "Decor team arrives and begins setup", "Decorator"],
        ["11:00 am", "Catering and drinks stations arrive", "Caterer"],
        ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]
t = Table(rows, colWidths=[70, 288, 136], rowHeights=[24] + [26] * 8)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 9),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 1), (-1, -1), 9),
    ("TEXTCOLOR", (0, 1), (-1, 2), HexColor("#8DA896")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, TINT]),
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
tw, th = t.wrap(W, H); t.drawOn(c, M, y - th); y -= th + 22

c.setFont("Helvetica-Bold", 11); c.setFillColor(NAVY); c.drawString(M, y, "Ask every vendor these six questions")
y -= 8
qs = ["Is my date available, and what do you need to hold it?",
      "What exactly is included, and what costs extra?",
      "What is the payment schedule and the cancellation policy?",
      "Who will be on-site on the day, and how many people?",
      "What is your backup plan if something goes wrong?",
      "Can I see photos or references from similar events?"]
for q in qs:
    y -= 6
    c.setStrokeColor(GOLD_D); c.setLineWidth(1); c.roundRect(M, y - 10, 9, 9, 2, stroke=1, fill=0)
    y -= para(q, body, M + 18, y, W - 2 * M - 18)

# CTA box
bh = 104; by = 66
c.setFillColor(NAVY); c.roundRect(M, by, W - 2 * M, bh, 12, stroke=0, fill=1)
c.setFillColor(GOLD); c.rect(M, by, 4, bh, stroke=0, fill=1)
c.setFont("Helvetica-Bold", 14); c.setFillColor(white); c.drawString(M + 22, by + bh - 28, "Want the details handled for you?")
para("Janeses brings catering, cakes, bridal services, decor, drinks and event essentials under one roof. "
     "Book a free consultation and we will turn this plan into a day your guests remember.", white_p,
     M + 22, by + bh - 38, W - 2 * M - 44)
c.setFont("Helvetica-Bold", 9.6); c.setFillColor(GOLD)
c.drawString(M + 22, by + 14, "WhatsApp / call: +234 803 889 3499     janesesconcept@gmail.com")
c.showPage()
c.save()
print("saved", OUT)
