(() => {
  const book = window.BOOK;
  const root = document.getElementById('book');
  const photoRoot = book.photoRoot || 'assets/photos/sample/';
  const params = new URLSearchParams(window.location.search);
  const mobileQuery = window.matchMedia('(max-width: 760px)');
  let mobileSide = params.get('side') === 'right' || Number(params.get('page') || 1) === 1 ? 1 : 0;
  const updatePreviewScale = () => document.documentElement.style.setProperty('--preview-scale', String(Math.min(1, (window.innerWidth - 20) / (mobileQuery.matches ? 600 : 1200))));
  updatePreviewScale();

  const fontFamilies = {
    poem: '"LXGW WenKai", "Album Kai", "KaiTi", serif',
    serif: '"Noto Serif SC", "Songti SC", "SimSun", "LXGW WenKai", serif',
    playful: '"Smiley Sans", "Microsoft YaHei", sans-serif',
    sans: '"Noto Sans SC", "Microsoft YaHei", "LXGW WenKai", sans-serif',
    latin: 'Georgia, "Times New Roman", serif'
  };

  const captionDesignStyle = (design = {}) => {
    const styles = [];
    const unit = value => typeof value === 'number' ? `${value}%` : value;
    if (design.x !== undefined) styles.push(`left:${unit(design.x)}`, 'right:auto');
    if (design.y !== undefined) styles.push(`top:${unit(design.y)}`, 'bottom:auto');
    if (design.right !== undefined) styles.push(`right:${unit(design.right)}`, 'left:auto');
    if (design.bottom !== undefined) styles.push(`bottom:${unit(design.bottom)}`, 'top:auto');
    if (design.width !== undefined) styles.push(`width:${unit(design.width)}`, 'max-width:none');
    if (design.font && fontFamilies[design.font]) styles.push(`font-family:${fontFamilies[design.font]}`);
    if (design.size) styles.push(`font-size:${design.size}`);
    if (design.color) styles.push(`color:${design.color}`);
    if (design.wrap === 'nowrap') styles.push('white-space:nowrap', 'text-wrap:initial');
    if (design.align) styles.push(`text-align:${design.align}`);
    if (design.lineHeight) styles.push(`line-height:${design.lineHeight}`);
    if (design.letterSpacing) styles.push(`letter-spacing:${design.letterSpacing}`);
    if (design.writingMode) styles.push(`writing-mode:${design.writingMode}`);
    if (design.background) styles.push(`background:${design.background}`);
    if (design.padding) styles.push(`padding:${design.padding}`);
    if (design.rotate !== undefined) styles.push(`transform:rotate(${design.rotate}deg)`);
    return styles.join(';').replaceAll('"', '&quot;');
  };

  const escapeHtml = value => String(value ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  const assetUrl = value => String(value).split('/').map(part => encodeURIComponent(part).replaceAll("'",'%27')).join('/');
  const protectShortTail = (line) => {
    const chars = [...line];
    if (chars.length <= 7) return escapeHtml(line);
    return `${escapeHtml(chars.slice(0, -4).join(''))}<span class="no-orphan">${escapeHtml(chars.slice(-4).join(''))}</span>`;
  };
  const copyHtml = value => value.split('\n').map((line, index) => {
    const protectedLine = protectShortTail(line);
    return index ? `<small>${protectedLine}</small>` : protectedLine;
  }).join('<br>');

  const textSeed = value => [...value].reduce((total, char) => total + char.codePointAt(0), 0);
  const automaticTypography = (text, family = 'editorial', tone = 'cream') => {
    const length = [...text.replace(/\s/g, '')].length;
    const expressive = family === 'zine' || family === 'poem';
    return {
      // Wider measures keep short Chinese tails from being stranded on their
      // own line; the placement pass then chooses an actual open pocket.
      width: length <= 10 ? '12em' : length <= 20 ? '17em' : '22em',
      font: expressive ? 'poem' : 'serif',
      size: length <= 10 ? 'clamp(19px, 1.62vw, 30px)' : length <= 22 ? 'clamp(16px, 1.33vw, 25px)' : 'clamp(14px, 1.1vw, 20px)',
      rotate: ((textSeed(text) % 9) - 4) / 2,
      align: 'left',
      lineHeight: expressive ? '1.4' : '1.55',
      tone
    };
  };

  const photoMarkup = (photo) => {
    if (photo.backgroundOnly) return ""; // Selected photo is rendered once as the spread background.
    const fit = photo.fit || 'cover';
    const position = photo.position || '50% 50%';
    const filter = photo.filter || 'none';
    const captionStyle = photo.captionStyle || 'note';
    const caption = photo.caption ? `<figcaption class="${captionStyle}">${escapeHtml(photo.caption)}</figcaption>` : '';
    const source = photo.path || `${photoRoot}${photo.file}`;
    const alt = photo.alt || photo.file || '装饰插画';
    const frame = photo.frame;
    const frameStyle = frame ? ' style="' + [`left:${frame.x}%`,`top:${frame.y}%`,`width:${frame.width}%`,`height:${frame.height}%`,`transform:rotate(${frame.rotate || 0}deg)`,`z-index:${frame.z || 1}`].join(';') + '"' : '';
    return `<figure class="photo${photo.edgeTreatment === 'night-blend' ? ' night-blend' : ''}"${frameStyle}><img data-src="${assetUrl(source)}" data-asset-id="${escapeHtml(photo.sourceAsset || source)}" alt="${escapeHtml(alt)}" style="--fit:${fit};--position:${position};--filter:${filter}" loading="eager" decoding="async">${caption}</figure>`;
  };

  const stickerMarkup = (sticker) => {
    const unit = value => typeof value === 'number' ? `${value}%` : value;
    const styles = [
      `left:${unit(sticker.x ?? 5)}`,
      `top:${unit(sticker.y ?? 5)}`,
      `width:${unit(sticker.width ?? 16)}`,
      `--sticker-rotate:${sticker.rotate ?? 0}deg`,
      `--sticker-opacity:${sticker.opacity ?? 1}`,
      `z-index:${sticker.z ?? 18}`
    ];
    const alt = sticker.alt || sticker.label || '手绘贴纸装饰';
    return `<figure class="page-sticker" data-sticker-id="${sticker.id || ''}" style="${styles.join(';')}"><img src="${assetUrl(sticker.path)}" alt="${escapeHtml(alt)}" loading="eager"></figure>`;
  };

  const pageMarkup = (page, side, spread) => {
    const hasSpreadCopy = side === 'left' && (spread.title || spread.note);
    const toneClass = page.tone ? ` tone-${page.tone}` : '';
    const captionHtml = page.caption ? copyHtml(page.caption) : '';
    const captionPlacement = page.captionPlacement || (page.captionDesign ? 'manual' : 'auto');
    const resolvedCaptionDesign = page.captionDesign || (captionPlacement === 'auto' ? automaticTypography(page.caption || '', page.family, page.tone) : null);
    const captionDesign = resolvedCaptionDesign ? ` data-design="true" style="${captionDesignStyle(resolvedCaptionDesign)}"` : '';
    const captionAuto = captionPlacement === 'auto' ? ` data-auto-place="true" data-prefer="${page.captionPrefer || 'balanced'}"` : '';
    const floatingNotes = (page.notes || []).map(note => {
      const placement = note.placement || (note.design ? 'manual' : 'auto');
      const design = note.design || automaticTypography(note.text, page.family, page.tone);
      const auto = placement === 'auto' ? ` data-auto-place="true" data-prefer="${note.prefer || 'balanced'}"` : '';
      return `<p class="floating-note ${note.style || ''}" data-design="true"${auto} style="${captionDesignStyle(design)}">${copyHtml(note.text)}</p>`;
    }).join('');
    const stickers = (page.stickers || []).map(stickerMarkup).join('');
    const generatedClass = spread.generatedAppend ? ' generated-append' : '';
    const artClass = page.backgroundPath ? ' has-art-background' : '';
    const pageStyle = page.backgroundPath ? ` style="--page-art:url('${assetUrl(page.backgroundPath)}');--page-art-opacity:${page.backgroundOpacity ?? .14}"` : '';
    return `
    <section class="page ${side} layout-page-${page.layout} family-${page.family || 'editorial'}${toneClass}${generatedClass}${artClass}${page.plainBackground ? " plain-background" : ""}${page.printDateContrast ? " print-date-contrast" : ""}"${pageStyle}>
      <div class="photo-grid layout-${page.layout}">${page.photos.map(photoMarkup).join('')}</div>
      ${stickers}
      ${side === 'left' && spread.eyebrow ? `<p class="spread-date">${escapeHtml(spread.eyebrow)}</p>` : ''}
      ${hasSpreadCopy ? `<div class="page-copy"><p class="eyebrow">${escapeHtml(spread.eyebrow || '')}</p>${spread.title ? `<h2>${escapeHtml(spread.title)}</h2>` : ''}${spread.note ? `<p class="note">${escapeHtml(spread.note)}</p>` : ''}</div>` : ''}
      ${page.caption ? `<p class="page-caption ${page.captionStyle || ''}"${captionDesign}${captionAuto}>${captionHtml}</p>` : ''}
      ${floatingNotes}
      ${page.letter ? `<div class="love-letter ${page.letter.style || ''}">${page.letter.paragraphs.map(text => `<p>${text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('\n', '<br>')}</p>`).join('')}</div>` : ''}
    </section>`;
  };

  const cover = document.createElement('article');
  cover.className = 'spread cover';
  const coverSource = book.cover.path || `${photoRoot}${book.cover.photo}`;
  const coverClass = book.cover.integratedText ? 'cover-front integrated-art' : 'cover-front';
  const coverCopy = book.cover.integratedText ? '' : `<div class="cover-copy"><h1>${escapeHtml(book.title)}</h1><p>${escapeHtml(book.subtitle)}</p></div>`;
  const backStyle = book.cover.backColor ? ` style="background:${book.cover.backColor}"` : '';
  const backImage = book.cover.backPath ? `<img src="${assetUrl(book.cover.backPath)}" alt="封底插画">` : '';
  cover.innerHTML = `
    <section class="cover-back${book.cover.backPath ? ' illustrated-back' : ''}" aria-label="封底"${backStyle}>${backImage}</section>
    <section class="${coverClass}" aria-label="正封面">
      <img src="${assetUrl(coverSource)}" alt="封面插画" style="--position:${book.cover.position}">
      ${coverCopy}
    </section>`;
  root.appendChild(cover);

  book.spreads.forEach((spread) => {
    const node = document.createElement('article');
    node.className = 'spread' + (spread.backgroundPhoto ? ' photographic-background' : '');
    const bg = spread.backgroundPhoto;
    const background = bg ? '<img class="spread-background-photo" data-src="' + assetUrl(bg.path) + '" alt="' + escapeHtml(bg.alt || bg.file) + '" style="object-position:' + (bg.position || '50% 50%') + ';filter:' + (bg.filter || 'none') + '" decoding="async">' : '';
    node.innerHTML = background + pageMarkup(spread.left, 'left', spread) + pageMarkup(spread.right, 'right', spread);
    root.appendChild(node);
  });

  const spreads = [...document.querySelectorAll('.spread')];
  let index = Math.max(0, Math.min(spreads.length - 1, Number(params.get('page') || 1) - 1));

  const required = new Set();
  book.spreads.forEach(spread => ['left', 'right'].forEach(side => spread[side].photos.filter(photo => !photo.decorative).forEach(photo => required.add(photo.file))));
  document.getElementById('status').textContent = `${required.size} 张照片`;

  const overlapArea = (a, b) => {
    const width = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
    const height = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    return width * height;
  };

  const rectangleGap = (a, b) => {
    const dx = Math.max(b.left - a.right, a.left - b.right, 0);
    const dy = Math.max(b.top - a.bottom, a.top - b.bottom, 0);
    return Math.hypot(dx, dy);
  };

  const placeAutomaticText = (page) => {
    const elements = [...page.querySelectorAll('[data-auto-place="true"]')];
    if (!elements.length) return;
    const pageRect = page.getBoundingClientRect();
    const safeX = pageRect.width * .048;
    const safeY = pageRect.height * .048;

    elements.forEach((element) => {
      element.style.visibility = 'hidden';
      element.style.left = '0';
      element.style.top = '0';
      element.style.right = 'auto';
      element.style.bottom = 'auto';

      const width = element.offsetWidth;
      const height = element.offsetHeight;
      const maxX = Math.max(safeX, pageRect.width - safeX - width);
      const maxY = Math.max(safeY, pageRect.height - safeY - height);
      const stepX = Math.max(14, pageRect.width * .035);
      const stepY = Math.max(12, pageRect.height * .035);
      const xs = [safeX, maxX, (safeX + maxX) / 2];
      const ys = [safeY, maxY, (safeY + maxY) / 2];
      for (let x = safeX; x <= maxX; x += stepX) xs.push(x);
      for (let y = safeY; y <= maxY; y += stepY) ys.push(y);

      const obstacles = [...page.querySelectorAll('.photo, .page-sticker, .page-copy, .spread-date, .page-caption:not([data-auto-place="true"]), .floating-note:not([data-auto-place="true"]), [data-auto-placed="true"]')]
        .filter(node => node !== element)
        .map(node => {
          const rect = node.getBoundingClientRect();
          return {
            left: rect.left - pageRect.left,
            top: rect.top - pageRect.top,
            right: rect.right - pageRect.left,
            bottom: rect.bottom - pageRect.top,
            text: node.matches('.page-caption, .floating-note, .page-copy, .spread-date, [data-auto-placed="true"]')
          };
        });

      const preference = element.dataset.prefer || 'balanced';
      let best = null;
      xs.forEach(x => ys.forEach(y => {
        const box = { left: x, top: y, right: x + width, bottom: y + height };
        const area = Math.max(1, width * height);
        let score = 0;
        let nearestGap = pageRect.width;
        obstacles.forEach(obstacle => {
          const overlap = overlapArea(box, obstacle) / area;
          score += overlap * (obstacle.text ? 24000 : 11000);
          nearestGap = Math.min(nearestGap, rectangleGap(box, obstacle));
        });
        score += Math.min(nearestGap / pageRect.width, .2) * 45;
        if (preference.includes('left')) score += (x / pageRect.width) * 35;
        if (preference.includes('right')) score += ((maxX - x) / pageRect.width) * 35;
        if (preference.includes('top')) score += (y / pageRect.height) * 22;
        if (preference.includes('bottom')) score += ((maxY - y) / pageRect.height) * 22;
        score += Math.abs((y + height / 2) / pageRect.height - .55) * 2;
        if (!best || score < best.score) best = { x, y, score };
      }));

      element.style.left = `${(best.x / pageRect.width) * 100}%`;
      element.style.top = `${(best.y / pageRect.height) * 100}%`;
      element.style.visibility = '';
      element.dataset.autoPlaced = 'true';
      element.dataset.autoX = ((best.x / pageRect.width) * 100).toFixed(1);
      element.dataset.autoY = ((best.y / pageRect.height) * 100).toFixed(1);
      if (best.score > 1000) element.dataset.placementWarning = 'overlap';
    });
  };

  const placeAllAutomaticText = () => {
    spreads.slice(1).forEach((spread) => {
      spread.classList.add('measure-active');
      spread.querySelectorAll('.page').forEach(placeAutomaticText);
      spread.classList.remove('measure-active');
    });
  };

  const render = () => {
    root.classList.toggle('mobile-right', mobileSide === 1);
    document.getElementById('mobileSide').textContent = mobileSide ? '右页' : '左页';
    spreads.forEach((spread, spreadIndex) => spread.classList.toggle('active', spreadIndex === index));
    // Warm nearby pages before the reader reaches them; keep distant originals unloaded.
    for (const offset of [0, 1, -1, 2, -2]) {
      const nearby = spreads[index + offset];
      if (!nearby) continue;
      nearby.querySelectorAll('img[data-src]').forEach(img => {
        img.loading = 'eager';
        img.fetchPriority = offset === 0 ? 'high' : 'low';
        if (!img.getAttribute('src')) {
          img.src = img.dataset.src;
          img.decode?.().catch(() => {});
        }
      });
    }
    document.getElementById('prevButton').disabled = index === 0 && (!mobileQuery.matches || mobileSide === 0);
    document.getElementById('nextButton').disabled = index === spreads.length - 1 && (!mobileQuery.matches || mobileSide === 1);
    document.getElementById('counter').textContent = spreads.length;
    document.getElementById('pageInput').max = spreads.length;
    document.getElementById('pageInput').value = index + 1;
    const nextUrl = new URL(window.location.href);
    nextUrl.searchParams.set('page', index + 1);
    if (mobileQuery.matches) nextUrl.searchParams.set('side', mobileSide ? 'right' : 'left');
    else nextUrl.searchParams.delete('side');
    history.replaceState(null, '', nextUrl);
  };

  const move = (delta) => {
    if (mobileQuery.matches) {
      const leaf = Math.max(0, Math.min(spreads.length * 2 - 1, index * 2 + mobileSide + delta));
      index = Math.floor(leaf / 2); mobileSide = leaf % 2;
    } else index = Math.max(0, Math.min(spreads.length - 1, index + delta));
    render();
  };
  document.getElementById('prevButton').addEventListener('click', () => move(-1));
  document.getElementById('nextButton').addEventListener('click', () => move(1));
  document.getElementById('pageJump').addEventListener('submit', (event) => {
    event.preventDefault();
    const requested = Number.parseInt(document.getElementById('pageInput').value, 10);
    if (!Number.isFinite(requested)) return;
    index = Math.max(0, Math.min(spreads.length - 1, requested - 1));
    mobileSide = index === 0 ? 1 : 0;
    render();
  });
  document.addEventListener('keydown', (event) => {
    if (event.target instanceof Element && event.target.closest('input, textarea, select, button, [contenteditable="true"]')) return;
    if (['ArrowLeft','ArrowRight',' ','Home','End'].includes(event.key)) event.preventDefault();
    if (event.key === 'ArrowLeft') move(-1);
    if (event.key === 'ArrowRight' || event.key === ' ') move(1);
    if (event.key === 'Home') { index = 0; mobileSide = 1; render(); }
    if (event.key === 'End') { index = spreads.length - 1; mobileSide = 1; render(); }
  });
  const finishLayout = () => {
    placeAllAutomaticText();
    render();
  };
  window.addEventListener('beforeprint', () => root.querySelectorAll('img[data-src]').forEach(img => { img.src = img.dataset.src; }));
  let resizeTimer;
  window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { updatePreviewScale(); render(); const active = spreads[index]; active.classList.add('measure-active'); active.querySelectorAll('.page').forEach(placeAutomaticText); active.classList.remove('measure-active'); }, 150); });
  let touchStart;
  root.addEventListener('touchstart', e => { const t=e.changedTouches[0]; touchStart={x:t.clientX,y:t.clientY}; }, {passive:true});
  root.addEventListener('touchend', e => {
    if (!touchStart || !mobileQuery.matches) return;
    const t=e.changedTouches[0], dx=t.clientX-touchStart.x, dy=t.clientY-touchStart.y;
    if (Math.abs(dx)>50 && Math.abs(dx)>Math.abs(dy)*1.5) move(dx<0?1:-1);
    touchStart=null;
  }, {passive:true});
  render();
  if (document.fonts?.ready) document.fonts.ready.then(finishLayout);
  else finishLayout();
})();
