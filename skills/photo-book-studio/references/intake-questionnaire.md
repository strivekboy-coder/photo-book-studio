# Fixed first-use questionnaire

Route an unclear request with the single mode question below; do not ask it again when the user already named a mode. Use the numbered album questionnaire once for a new ordinary photo book. Standalone Plog uses the optional one-message preference prompt and safe defaults, not the numbered album questions. Ask it in the user's language and preserve the numbered choices. Infer answers the user has already supplied and omit only those answered items. Do not merge the creative-permission questions into one long question.

Tell the user they may reply with compact choices such as `1. ... 2C 3E`, write `由你推荐` / `recommend`, or accept every recommended option.

## 先选制作模式（只在请求不明确时询问）

**你想做相册，还是 Plog／手账？**

- A. 相册：继续下面的相册问卷。
- B. Plog／手账：**后面的相册问卷不用回答**，直接进入轻量设计流程。

用户已经明确说要做相册或 Plog 时，不重复问这题。只说“帮我整理这些照片”且用途不明确时，先单独问模式，不要同时抛出整个相册问卷。手账风的印刷相册仍走相册路线；只有明确涉及实体成册时再补相关输出问题。

## Plog：一条可跳过的偏好提示

> 有喜欢的风格、参考图、想写的文字或指定贴纸，可以一起发给我；没有偏好，也可以直接让我根据照片设计。

这不是另一套必填问卷。已有照片，用户明确要看效果、让 AI 设计或已经给了参考时，直接使用已有信息与安全默认项开始；不要求回答这条提示后才制作。缺少照片时只请求照片；只有一个未解决事项会实质影响结果时才补问该事项。

默认做竖版3:4分享页，保留所有选图各一次，照片多时安排能清楚容纳它们的页面组，不因“试效果”偷偷遗漏。文案只根据已知信息与可见内容写少量草稿，未知地点、日期、关系不猜。普通裁切/图层排版和与故事相关的装饰按请求设计，原图只读；不默认重画人物、替换原照、公开作品或导出 PDF。默认提供分享图片与带微调的 HTML，明确只要图片时遵循用户选择。既有明确偏好优先于这些默认项。

开始前仍要把明确偏好与推断默认项保存到 brief 并标注来源；`intakeComplete` 表示这次制作所需信息已经可用，不表示用户填写了整套相册问卷。之后按短流程执行读图分组、视觉方向与适配路线选择、整合生成或基础排版加手绘增强、实际成图审核和照片完整性检查。研究网站、素材下载、字体比较按需要调用，不再每次必做。

## 相册问卷（仅选择相册后使用）

## 一、相册基本信息

**1. 这本相册送给谁，记录什么故事和时间范围？**

请用一两句话说明。

**2. 最终需要什么成品？**

- A. 印刷相册
- B. 网页相册
- C. 印刷和网页都要
- D. 还没决定

**3. 版型和尺寸怎么确定？**

- A. 已有打印平台或具体尺寸
- B. 方形
- C. 横版
- D. 竖版
- E. 先分析照片，再由你推荐（推荐）

## 二、照片与篇幅

**4. 上传的照片是否都要入册？**

- A. 全部入册（默认）
- B. 我会标记哪些照片可以不用
- C. 允许你提出建议，但最终由我决定

**5. 照片怎么上传？**

- A. 先上传 30–50 张代表照片做样稿（推荐）
- B. 按每批 50–80 张分批上传
- C. 一次上传全部照片

**6. 希望整本相册是什么节奏？**

- A. 留白较多，大图较多
- B. 疏密结合，有重点也有生活碎片（推荐）
- C. 图片丰富紧凑
- D. 看完照片后，由你推荐节奏

**6b. 是否有印刷预算或最多页数？（可跳过）**

- A. 暂时不限，优先保证照片舒展（推荐）
- B. 我有预算或页数上限：____
- C. 还不确定，先做样稿再估算

预算仅用于讨论篇幅取舍，不承诺未确认的印刷价格；页数需说明是单页还是跨页。

## 三、风格与文字

**7. 希望相册是什么视觉感觉？**

可以选择 2–4 个：干净、可爱、温暖、活泼、诗意、复古、zine 杂志感、手账感、极简，或由我根据照片推荐。用户也可以提供相册、海报或网页参考图。

若用户只说“zine”且参考图还不能明确方向，在第7题附一个短选择：A. 极简编辑式；B. 高饱和拼贴；C. 纸感手作；D. 看照片后推荐。已有明确偏好就不再问，将方向保存到 brief.visual。

**8. 文案从哪里来？**

- A. 我提供描述，你负责润色
- B. 你根据照片中能看到的内容写，不虚构具体经历
- C. 两者结合：有描述就润色，没有就适当补充（推荐）
- D. 尽量少写，只保留日期和标题

**9. 如果使用文字，希望是什么风格？**

可以选择 1–2 个：温柔诗意、可爱俏皮、日记口吻、幽默活泼、纪实克制、简短留白，或由我根据不同事件灵活决定（推荐）。同时询问中文、英文或中英混合。

## 四、照片处理与创意元素

**10. 是否允许基础照片优化？**

- A. 可以裁剪、提亮和统一色彩，但保留真实感（推荐）
- B. 只能提亮和调色，不能裁剪
- C. 不处理原图

**11. 是否希望根据照片内容加入贴纸？**

例如花、雪山、交通工具、食物或节日元素。

- A. 可以，适量点缀（推荐）
- B. 可以丰富一些
- C. 不需要贴纸

**12. 封面怎么制作？**

- A. 根据相册故事绘制专属插画封面（默认推荐）
- B. 使用我选中的照片
- C. 做纯文字或极简封面
- D. 看完照片后提供两种方向让我选择

默认先完成内页并审核整本故事，再用可用的 image 工具制作最终封面；小样先使用占位封面。选择照片或纯文字封面时遵循你的选择。

**13. 是否使用撕纸照片效果？**

它会保留真实照片，同时把部分边缘变成不规则纸张或插画结构。

- A. 只在特别合适的少数页面使用（推荐）
- B. 可以多使用一些
- C. 不使用

**14. 是否允许把部分照片制作成艺术衍生图？**

这种方式用于合适的照片、建筑、风景或章节过渡页。会评估七条创意路线，按你允许的处理与真实照片选择；不要求使用全部效果。

- A. 保留原图，衍生图只作背景或装饰（推荐）
- B. 特别合适时可以替换原图，但必须标出来供我审核
- C. 不制作艺术衍生图

**15. 是否需要“照片简化”设计？**

它会从照片提取颜色、轮廓或局部元素，制作成简洁的小卡片、色块画或抽象陪衬页。

- A. 可以，在适合的页面少量使用（推荐）
- B. 可以作为较明显的视觉特色
- C. 不需要

## After the answer

1. Resolve any direct questions in the user's response, including upload strategy or format recommendations.
2. Ask a follow-up only when an unanswered ambiguity would materially change the sample.
3. Save every answer and accepted recommendation to `project/brief.json` before arranging photos.
4. Record whether each value was `explicit`, `recommended_accepted`, `inferred`, or still `unknown`.
5. Start with a representative sample when that route was chosen.
6. Never repeat this questionnaire for later batches or local revisions. Read the saved brief instead.
