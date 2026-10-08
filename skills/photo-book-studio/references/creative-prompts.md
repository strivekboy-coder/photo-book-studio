# Source-linked creative prompts

Read for a selected route 5, 6 or 7 after the seven-route suitability review. These are adaptable production briefs, not default treatments for every album or Plog. Use the current user's actual photos and confirmed facts. Preserve all selected memories and saved permissions. Persist the filled prompt and inspect the result; writing the constraints does not establish that they were achieved.

## 5. Travel-envelope adaptation

Reference: [HwawH-J-Y/travel-envelope](https://github.com/HwawH-J-Y/travel-envelope). Reviewed 2026-10-08. The repository provides photo-role selection, source relationships, an imagegen prompt and visual acceptance checks, rather than a separate rendering program. No repository license file was established during this review; this skill links to it and uses the independently authored adaptation below rather than copying its full instructions or prompt. Consult the official skill if the user explicitly wants its exact workflow. Its omission/repetition and automatic local-object options never override this skill's source-preservation policy.

Before generating: designate one scenic source, distinct foreground sources, a calm paper hue from the photos, the pocket's occlusion order and a known title or no text. Do not add destination souvenirs merely because inputs are sparse. Describe every permitted new decoration separately.

```text
Make one 3:4 photographic travel keepsake collage using these designated sources:
{background ID and its visible place/context}; {each foreground source ID, unique
photo region or subject, frame/cutout treatment and intended position}.
Keep the background recognizable and fill the canvas with that actual scene.
Place a thin open paper envelope as a graphic overlay, roughly three-fifths of
the width, with generous scenery around it. Choose a pale, subdued paper color
from {actual photo colors}. The envelope does not stand on the photographed
ground and casts no shadow onto the scene. Its folds remain shallow.
Build one uneven but balanced cluster: back prints emerge at different heights;
the source focal subject sits off center; the front pocket hides their lower
edges. Use real overlap rather than separated columns. Preserve identities,
objects, perspective and visible source details. Keep difficult contours in
framed photographs instead of rebuilding them. No white cutout halo.
Use each designated source once. Do not clone a person or add unseen anatomy.
Only the envelope, photo mounts, paper texture and subtle layer-contact shading
may be newly created, plus {explicitly allowed decorative additions, or NONE}.
Text: {exact confirmed wording, or NONE}, small and quiet on the paper front.
No invented date, ticket, stamp value, itinerary, brand, slogan or watermark.
Avoid oversized kraft boxes, muddy sepia, theatrical shadows and a rigid grid.
```

Inspect whole-group scale, scenery visibility, subject fidelity and pocket overlap. A 2026-10-08 four-source stock-photo trial initially made the envelope too large and grounded on the street; one scale/shadow correction produced a clearer flat overlay. This is a promising trial, not universal proof of fidelity or expert quality.

## 6. Subject breaks the frame — user-provided prompt

The following prompt was supplied by the project user; keep its visual invariants. Identify the actual viable subject before filling a tool request. No new text is implied. A complete contour may be a person, architectural element, plant, animal or another recognizable visible subject. Do not reconstruct unseen portions.

```text
请将我上传的照片作为唯一主要视觉来源，把它重新设计成一张具有摄影拼贴感和现代平面设计感的「主体突破画框」作品。
不要重新创造一个完全不同的场景，也不要简单给照片增加边框。
请先分析原照片的主体、背景和空间层次，自动识别其中最适合被完整保留并突破画框的视觉主体，例如：树枝、树干、人物、建筑、花朵、植物、山体、云层、海浪、路灯、电线或其他具有明确轮廓的元素。

然后按照以下方式重新组织画面：
1. 将整体背景处理为大面积干净的白色或自然暖白色留白。
2. 在画面中央设置一个简洁的大尺寸矩形摄影窗口。
3. 矩形内部保留原照片的局部完整场景和背景关系，不要变成单纯色块，也不要重新生成无关景物。
4. 将原照片中最重要的主体精确分离出来，并置于矩形摄影窗口的上层。
5. 主体的一部分位于矩形内部，另一部分自然延伸、穿越并突破矩形边缘，进入外部白色留白区域。
6. 矩形边界必须干净、笔直、明确；但主体经过的位置不受矩形裁切，形成真实的前后图层穿插关系。
7. 保留主体原有的形状、姿态、枝干走势、比例、透视、纹理和主要颜色，尽量让人能够认出它来自原照片。
8. 不要额外增加原照片中不存在的大量装饰元素，不要把主体重新画成插画，不要制造明显 AI 风格。
整体效果类似摄影作品经过精细抠图和图层蒙版重新排版：
白色画布 + 中央矩形原照片窗口 + 原照片主体跨越矩形边界。
画面应自然、克制、有呼吸感，具有摄影杂志、艺术书籍和编辑设计感。
可以根据原照片的构图自动调整矩形的位置、大小和比例，使主体突破边界的位置最自然、最有视觉张力。
如果原图本身存在天空、墙面、水面等较纯净背景，可以优先将其保留在矩形窗口内部，以增强主体与背景之间的色块反差。
禁止：
不要给整个照片简单套一个矩形边框；
不要把主体全部困在矩形内部；
不要让整个照片都铺满画布；
不要随意改变主体结构；
不要出现重复树枝、重复人物、多余肢体或无意义物体；
不要添加明显阴影让它变成悬浮卡片；
不要做成普通海报模板。
```

An early stock panda trial showed the mechanism but the user rejected its source choice for the intended aesthetic; it is not an approved quality example. A later tree/park-building trial better matched the requested photographic language. Generated fur and fine foliage are still derivative pixels; do not certify unchanged originals. A literal source mask is preferable when fidelity must be exact.

## 7. Three-photo paper collage — user-provided prompt

```text
请把我上传的三张照片做成竖版3:4手帐拼贴。选择一张作为中央主图，另外两张裁成一横一竖的辅助照片，必要时降低饱和度或转成黑白。拼贴主体约占画面 45%，四周保留大面积米白色留白。加入10-15 层撕纸、硫酸纸、活页纸、信封和少量彩色色块，层次丰富但不要杂乱；素材颜色从照片中提取，胶带不要默认黑色。保留原照片内容，不添加文字、标志或水印。
```

Assign the three source roles from actual aspect ratios and safe crops. Do not apply these 45%/10–15-layer references to other Plog pages. Existing words within a photograph are source content, not permission to add a title. Keep paper colors connected to photos, with a true landscape/portrait contrast. The initial red-colonnade/street/panda trial was rejected because the subjects were visually competing and the result read as separate photo cards. Later coffee/park/architecture studies used one central main image and partially covered support strips; a uniform scale correction improved the reference-like quiet silhouette. The initial failures stay review criteria, not advertised sample quality. Exact occupancy and layer count were not measured or certified. Keep the rendered photos truthful; the exact same layout can instead be made from original photo layers and generated/native paper materials.
