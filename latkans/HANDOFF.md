# Paste this into Claude Code on the Atreya PC (DESKTOP-20JHCT2)

```
Post the new Atreya Ganesh lotus bell latkan on Amazon.in and Flipkart today.

Everything is prepared in github.com/anjnusual/atreya-listing-assets, branch
claude/gifted-pascal-nzunb5, folder latkans/. Clone or pull it next to
E:/atreya/listing/atreya-aplus. Read latkans/README.md and latkans/listing.json first.
Copy and prices are final: Pack of 2 Rs 249 (MRP 599), Pack of 4 Rs 399 (MRP 999),
25 in stock each, size and weight are approved.

1. Redo the gallery images with our Azure image model (GPT image deployment in our .env),
   because the current renders look plain. First pull BhogKart's live Amazon images
   (SP-API catalog, e.g. B0HHPHVJ42) and match their look: layout, colour, typography.
   Use the photos in latkans/source/ as the input for every image. Never let the model
   redraw or change the product itself: the Ganesha plaque, lotus buds, bells, flowers and
   pearl tassel must stay exactly as photographed. Keep main.jpg as it is (pure white,
   real photo). Redo other1 to other8 and the aplus/ images with the same message per
   image as now (see README table and the text in tools/make_images.py; sizes are fixed:
   gallery 1600x1600, A+ header 1940x1200, A+ tiles 600x600). Overwrite the same file
   names, show me the set, then commit and push to the same branch.
2. Amazon: from latkans/, run
   node amazon_push.mjs listings            (fix any ERROR issues)
   node amazon_push.mjs listings --live
   node amazon_push.mjs status              (repeat until both SKUs have ASINs)
   node amazon_push.mjs aplus --live
3. Flipkart: create both SKUs in the Toran vertical using the flipkart block in
   listing.json and the same images (Seller Hub catalog upload if the API can't create a
   new product), then node flipkart_push.mjs --fsn2 <FSN> --fsn4 <FSN> --live.
4. Give me the amazon.in/dp and flipkart.com links for both packs.
```
