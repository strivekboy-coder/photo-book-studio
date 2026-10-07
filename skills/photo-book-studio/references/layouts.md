# Starting layouts

Prefer `layout: composed` for new custom pages. Supply each photo's percentage `frame` (x, y, width, height, rotate, z), `fit` and `position`. Add a manual captionDesign only after choosing actual whitespace. Do not cover or crop defining subjects; the simple examples below are candidates, not prescriptions.

- Hero: one frame roughly x8/y6/w84/h75, with open text space below or beside it.
- Pair: two 44%-width frames or two stacked 37%-height frames; choose according to real aspect ratios.
- Hero + two details: a large frame occupying about half the page, two smaller companions sharing the remaining calm region.
- Open four: adapt four distinct frame rectangles and give one a modest size lead; meaningful couple portraits should not be squeezed into equal tiny slots.
- Daily fragments: five/six frames only when content remains legible at the intended print size; add another spread otherwise.

Empty pages use `layout: empty`, `photos: []`. Background color can use `tone`; available base tones include cream, sky, sage, parchment, blush and white. A color not in the engine should be implemented deliberately in the renderer rather than silently assumed supported. Source-derived backgrounds use backgroundPath and opacity. Letters use paragraph-aware `letter`, not caption markup.

The engine includes older custom layout classes from its development project, but they are not required for new books. Choose `composed` or a suitable existing family; don't read or repeat every legacy selector. After changing page aspect ratio, reconsider frame/caption coordinates and re-render instead of copying percentages blindly.

For photographic narrative references, see photographic-layouts.md: panoramic anchor/inset, environmental hero/detail field, narrow photo column and quiet photo/text pause. These extend the starting structures without assigning one style to every book.
