/* =====================================================================
   PROMOTIONS: edit this file to add, change or remove offers on the
   home page. No HTML, no build step. Save, upload, refresh.

   HOW IT WORKS
   - Promos show in the order listed here.
   - "active": false  hides a promo without deleting it.
   - "start" / "end"  (optional, format "2026-12-31"): the promo appears only
     inside that window and disappears by itself the day after "end".
   - "image": the NAME of a photo in images-src/ (without extension) after you
     have run  python tools/optimize-images.py . Add a clear "alt" description.
   - If every promo is inactive or expired, the whole promo area disappears.

   LAYOUTS
   - "feature": dark card, text on the left, image on the right.
   - "menu":    image on the left, text + price table on the right.
   - "notice":  slim announcement band (no image), for short messages.

   BUTTONS (up to 3): { label, whatsapp: "pre-filled message" }  or  { label, href: "page.html" }
   "style" can be: "gold" (main), "navy" (dark), "outline".
   ===================================================================== */
window.JANESES_PROMOS_CONFIG = { whatsapp: "2348038893499" };

window.JANESES_PROMOS = [
  {
    id: "grab-and-go",
    active: true,
    layout: "feature",
    eyebrow: "Now on the menu",
    title: "The Grab & Go Combo.",
    text: "A freshly made shawarma with a chilled Janeses Zobo, ready when you are. Perfect for office lunches, staff treats and guests on the move. Order straight from WhatsApp, or ask us about bulk orders for your next event.",
    image: "combo-flyer",
    alt: "Janeses Loaded Grab and Go Combo flyer showing a Zobo drink and a shawarma",
    buttons: [
      { label: "Order on WhatsApp", whatsapp: "Hello Janeses, I'd like to order the Grab & Go Combo", style: "gold" },
      { label: "See Catering", href: "services.html#catering", style: "outline" }
    ]
  },
  {
    id: "special-combo-deal",
    active: true,
    layout: "menu",
    eyebrow: "Special combo deal",
    title: "Pair any treat with a chilled drink.",
    text: "Choose your favourite bake or snack and add a Janeses yoghurt or a 35cl zobo for less. Perfect for office orders, school runs and quick treats.",
    image: "combo-deal-final",
    alt: "Janeses Special Combo Deal flyer listing banana bread, cake parfait, cake slice, shawarma, meat pie, iced cupcakes and doughnuts with yoghurt or zobo prices",
    table: {
      caption: "Special combo deal prices",
      head: ["Treat", "+ Yoghurt", "+ Zobo 35cl"],
      rows: [
        ["Banana Bread", "₦5,000", "₦4,500"],
        ["Cake Parfait", "₦4,000", "₦3,500"],
        ["Cake Slice", "₦3,500", "₦3,000"],
        ["Shawarma", "₦5,000", "₦4,500"],
        ["Meat Pie", "₦2,500", "₦2,000"],
        ["Iced Cupcakes (6 pcs)", "₦4,000", "₦3,500"],
        ["Doughnut", "₦2,000", "₦1,500"]
      ]
    },
    buttons: [
      { label: "Order on WhatsApp", whatsapp: "Hello Janeses, I'd like to order from the Special Combo Deal", style: "navy" }
    ],
    note: "Suite 5 & 6, Sunny Peace Plaza, Jos"
  }

  // ---- EXAMPLE (a short notice). To use it: delete the two // at the start of each line,
  // add a comma after the closing brace of the promo above, then edit and save. ----
  // {
  //   id: "christmas-notice",
  //   active: true,
  //   layout: "notice",
  //   start: "2026-12-01",
  //   end: "2026-12-24",
  //   eyebrow: "Festive season",
  //   title: "Christmas cake orders are open.",
  //   text: "Book early so we can reserve your date.",
  //   buttons: [{ label: "Order a Cake", whatsapp: "Hello Janeses, I'd like to order a Christmas cake", style: "gold" }]
  // }
];
