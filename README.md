# Photo Book Studio

### 照片进来，故事成册。

把照片和几句描述交给 Codex，做成一本有自己的文字、排版、贴纸和专属封面的相册。

[![三本示例相册的专属封面](docs/showcase-hero.png)](https://strivekboy-coder.github.io/photo-book-studio/)

**[打开作品展示 ↗](https://strivekboy-coder.github.io/photo-book-studio/)** · **[下载 Skill](https://github.com/strivekboy-coder/photo-book-studio/releases)**

## 先翻三本小书

| 猫咪日常 | 情侣日记 | 旅行纸刊 |
|---|---|---|
| [今天也很会偷懒](https://strivekboy-coder.github.io/photo-book-studio/showcase/cat/) | [和你，慢慢来](https://strivekboy-coder.github.io/photo-book-studio/showcase/couple/) | [慢一点，慕尼黑](https://strivekboy-coder.github.io/photo-book-studio/showcase/munich/) |
| 6张照片，把家变软。 | 10张照片，把日常写成情书。 | 17张照片，把风景装进口袋。 |

![猫咪相册内页：哈欠、巡逻与手绘贴纸](docs/showcase/cat/spread-03.jpg)

![情侣相册内页：回家的路与金色拥抱](docs/showcase/couple/spread-04.jpg)

## 好看的，不只是封面

- **你的照片，都好好放进书里。** 不因相似或难排版而偷偷删掉回忆。
- **排版跟着故事走。** 大图、留白、拼贴、侧排与竖排，让重要的照片有自己的位置。
- **文字有自己的口吻。** 可爱的小批注、日记里的旁白、写给恋人的一句话。
- **封面从整本故事里长出来。** 默认先完成内页，再用可用的 image 工具画最终封面。
- **做完能翻，也能印。** 浏览器相册、手机单页阅读、网页打包与带出血的 PDF。

## 照片之外，再留一点感觉

| 给一个哈欠留白 | 把牵手变成记忆 | 让风景走出照片 | 寄给下一次出发 |
|---|---|---|---|
| ![极简纸刊](docs/showcase/effects/minimal.jpg) | ![抽象记忆](docs/showcase/effects/editorial.jpg) | ![撕纸插画](docs/showcase/effects/gathered.jpg) | ![旅行明信片](docs/showcase/effects/postcard.jpg) |
| Minimal Zine Poster | Photo Abstract Editorial | Gathered Scenes | Photo to Zine Postcard |

四种创意路线都已经用在示例里。它们按照片和故事选择，额外风格 skill 是可选增强。

![慕尼黑相册：真实冲浪照片与撕纸插画](docs/showcase/munich/spread-04.jpg)

## 开始做你的一本

需要 **Python 3.10+、Node.js 20.11+**。基础预览只需要 Pillow，不要求额外创意 skill。

```sh
git clone https://github.com/strivekboy-coder/photo-book-studio.git
cd photo-book-studio
python -m pip install -r requirements.txt
python scripts/install_skill.py --destination /your/codex/skills
```

Windows 可把 destination 换成自己的 Codex skills 目录。也可手动把 `skills/photo-book-studio` **整个文件夹**复制过去；其中包含模板、字体和工具，不要只复制 SKILL.md。重新打开会话使新 skill 被发现。

对 Codex 说：

> 使用 $photo-book-studio，我想给家人做一本相册。先问我必要的问题，问卷之后我再提供照片和故事。

制作时所有资料放在你自己的工作项目里，原照片保持只读。首次先做有代表性的小样；后续按批追加，不重跑整本流程。

## 命令行工具

这些命令提供可靠的初始化、清单、渲染与导出。**它们不会自动读懂照片、写故事或替代模型的审美审核。**

```sh
python skills/photo-book-studio/scripts/studio.py init /your/book --title "我们的故事"
# 填好问卷并保存 /your/book/project/brief.json，令 intakeComplete 为 true，再导入：
python skills/photo-book-studio/scripts/studio.py inventory --workspace /your/book --photos /your/selected-photos
# 模型根据联系表和描述填写 project/book.json 后：
node /your/book/scripts/build.mjs
python skills/photo-book-studio/scripts/studio.py web --workspace /your/book
```

浏览器打开项目的 `sample.html`。网页发布文件夹位于 `output/web-publish`；服务器上线是单独的操作，打包不等于已经上线。默认不附带登录或音乐，也不把前端生日谜题当访问保护。

## 印刷 PDF

```sh
python -m pip install -r requirements-print.txt
python -m playwright install chromium
python /your/book/scripts/export_pdf.py --workspace /your/book
```

已安装 Edge/Chrome 时也可用 `--browser /path/to/browser`，无需另下载 Chromium。

- 输出 `reading.pdf`、`interior.pdf`、`cover.pdf` 和 `preflight.json`。
- 页数与尺寸读取当前书稿，不固定到某一本书；四周按配置补出血。
- 默认单页正文前补一面，让原来的左/右跨页分别落在左/右位置；尾部按印厂页数倍数补齐，填字和底色可配置。
- 采用固定布局的光栅导出以保持浏览器排版；300dpi 导出不会增加原图细节，文字不保持可搜索状态。
- 内页出血不等于硬壳封面包边。封面、书脊、沟槽仍按印厂模板适配后确认。
- 默认方形 210×210mm。横/竖尺寸可以配置，但每种新比例都须重新视觉审核，不能沿用旧坐标直接宣称适合印刷。

详见 [使用与印刷说明](docs/USAGE.md)。


## 制作过程

第一次用简短问卷确定故事与偏好 → 看照片、做小样 → 分批补完整本 → 渲染检查 → 画最终封面 → 导出。

问卷只做一次；后续改文案、挪贴纸、调裁切只处理相关页。原照片保持只读，照片身份与次数由构建检查。

[详细使用与印刷说明](docs/USAGE.md) · [测试记录](docs/QA.md)

## 示例与许可

示例为效果展示，非真实用户故事；人物／动物关系、日期和文案为策展设定。摄影素材来自 Unsplash（含授权素材）及用户提供的授权图库，AI封面、插画和贴纸由image生成。图片与相册成品不属于代码的MIT许可范围，未经许可请勿转载。详细许可信息由维护者补充，见[素材说明](examples/README.md)。

项目自有代码与流程采用 [MIT](LICENSE)，字体保留 [SIL OFL](NOTICE.md)。基础功能无需额外创意 skill；印刷封面仍需按印厂包边／沟槽模板确认。
