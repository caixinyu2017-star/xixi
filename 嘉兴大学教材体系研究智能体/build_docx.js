// Build the Chinese design-plan Word document from plan.md
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, HeadingLevel, BorderStyle, ShadingType, ShadingType: ST,
  PageBreak, TableOfContents, Header, Footer, PageNumber, LevelFormat, LineRuleType,
  Tab, TabStopType, LeaderType,
  VerticalAlign, PageOrientation, convertMillimetersToTwip,
} = require('docx');

const SRC = path.join(__dirname, 'plan.md');
const OUT = process.argv[2] || path.join(__dirname, '嘉兴大学禾章智能体框架设计方案.docx');

const SONG = { ascii: 'Times New Roman', eastAsia: '宋体', hAnsi: 'Times New Roman' };
const HEI = { ascii: 'Arial', eastAsia: '黑体', hAnsi: 'Arial' };
const KAI = { ascii: 'Times New Roman', eastAsia: '楷体', hAnsi: 'Times New Roman' };
const MONO = { ascii: 'Consolas', eastAsia: '等线', hAnsi: 'Consolas' };

const NAVY = '1B3A6B';
const RED = 'C42B1C';
const GRAYBG = 'F2F4F7';
const HEADBG = 'E3E8F0';

// ---------- PNG dimension reader ----------
function pngSize(file) {
  const buf = fs.readFileSync(file);
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

// ---------- inline markdown (**bold**) -> TextRun[] ----------
function runs(text, opts = {}) {
  const base = { font: opts.font || SONG, size: opts.size || 24, color: opts.color };
  const out = [];
  const parts = text.split('**');
  parts.forEach((seg, i) => {
    if (seg === '') return;
    out.push(new TextRun({ ...base, text: seg, bold: i % 2 === 1 || !!opts.bold }));
  });
  if (out.length === 0) out.push(new TextRun({ ...base, text: '' }));
  return out;
}

function body(text, extra = {}) {
  return new Paragraph({
    children: runs(text),
    spacing: { line: 380, before: 60, after: 60 },
    indent: { firstLine: 480 },
    alignment: AlignmentType.JUSTIFIED,
    ...extra,
  });
}

// ---------- markdown parse ----------
const raw = fs.readFileSync(SRC, 'utf8').split('\n');
const children = [];

// ===== Cover page =====
const gap = (n = 1) => { for (let i = 0; i < n; i++) children.push(new Paragraph({ children: [new TextRun({ text: '', size: 24 })] })); };

gap(3);
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: '嘉 兴 大 学', font: HEI, size: 36, bold: true, color: NAVY })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 600 },
  children: [new TextRun({ text: '中国特色高质量教材体系研究智能体', font: HEI, size: 30, color: NAVY })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 160 },
  children: [new TextRun({ text: '「 禾 章 」', font: HEI, size: 64, bold: true, color: RED })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 700 },
  children: [new TextRun({ text: '框 架 设 计 方 案', font: HEI, size: 48, bold: true, color: NAVY })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  border: { top: { style: BorderStyle.SINGLE, size: 8, color: RED, space: 6 }, bottom: { style: BorderStyle.SINGLE, size: 8, color: RED, space: 6 } },
  spacing: { before: 200, after: 200 },
  children: [new TextRun({ text: '只做助研，不做代笔；只供证据，不出定论', font: KAI, size: 28, color: RED, bold: true })],
}));
gap(4);
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 100 },
  children: [new TextRun({ text: 'HeZhang Research Agent for the Textbook System', font: { ascii: 'Times New Roman', eastAsia: '宋体', hAnsi: 'Times New Roman' }, size: 22, color: '666666' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 400 },
  children: [new TextRun({ text: 'with Chinese Characteristics（HZ-Agent）', font: { ascii: 'Times New Roman', eastAsia: '宋体', hAnsi: 'Times New Roman' }, size: 22, color: '666666' })],
}));
gap(2);
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: '二〇二六年', font: HEI, size: 28 })],
}));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== TOC page =====
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 300 },
  children: [new TextRun({ text: '目　　录', font: HEI, size: 36, bold: true, color: NAVY })],
}));
const tocInsertAt = children.length;
children.push(new Paragraph({ children: [new PageBreak()] }));
const tocEntries = [];
const PAGEMAP = fs.existsSync(path.join(__dirname, 'pages.json'))
  ? JSON.parse(fs.readFileSync(path.join(__dirname, 'pages.json'), 'utf8')) : {};

// ===== Body =====
let i = 0;
let firstChapter = true;
let numInstance = 0;

function flushTable(lines) {
  const rowsRaw = lines
    .map(l => l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim()));
  const headerCells = rowsRaw[0];
  const dataRows = rowsRaw.filter((r, idx) => idx !== 1); // drop separator row
  const nCols = headerCells.length;
  const TOTAL = 9060; // dxa, fits A4 with 25mm margins
  // weight first column narrower when many columns
  const colW = [];
  if (nCols === 2) { colW.push(2600, TOTAL - 2600); }
  else if (nCols === 3) { colW.push(2000, 3600, TOTAL - 5600); }
  else if (nCols === 4) { colW.push(1500, 2400, 2600, TOTAL - 6500); }
  else if (nCols === 5) { colW.push(1300, 2000, 2100, 2100, TOTAL - 7500); }
  else {
    const w = Math.floor(TOTAL / nCols);
    for (let c = 0; c < nCols; c++) colW.push(c === nCols - 1 ? TOTAL - w * (nCols - 1) : w);
  }

  const trs = dataRows.map((cells, rIdx) => new TableRow({
    tableHeader: rIdx === 0,
    children: Array.from({ length: nCols }, (_, c) => new TableCell({
      width: { size: colW[c], type: WidthType.DXA },
      shading: rIdx === 0
        ? { type: ShadingType.CLEAR, fill: HEADBG, color: 'auto' }
        : { type: ShadingType.CLEAR, fill: rIdx % 2 === 0 ? GRAYBG : 'FFFFFF', color: 'auto' },
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 60, bottom: 60, left: 90, right: 90 },
      children: [new Paragraph({
        alignment: rIdx === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { line: 300, before: 20, after: 20 },
        children: runs((cells[c] || '').replace(/<br\s*\/?>/g, ' '), { size: 21, bold: rIdx === 0, font: rIdx === 0 ? HEI : SONG }),
      })],
    })),
  }));

  children.push(new Table({
    columnWidths: colW,
    width: { size: TOTAL, type: WidthType.DXA },
    alignment: AlignmentType.CENTER,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: NAVY },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY },
      left: { style: BorderStyle.SINGLE, size: 2, color: '9AA6BC' },
      right: { style: BorderStyle.SINGLE, size: 2, color: '9AA6BC' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: '9AA6BC' },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: '9AA6BC' },
    },
    rows: trs,
  }));
  children.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: '', size: 12 })] }));
}

while (i < raw.length) {
  const line = raw[i];
  const t = line.trim();

  // horizontal rule / blank
  if (t === '' || t === '---') { i++; continue; }

  // document title (cover already made)
  if (/^# /.test(t)) { i++; continue; }

  // images
  const im = t.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
  if (im) {
    const file = path.join(__dirname, im[2]);
    const { w, h } = pngSize(file);
    const MAXW = 580, MAXH = 790;   // px @96dpi; MAXH keeps tall figures inside one A4 page
    let dw = MAXW, dh = Math.round(MAXW * h / w);
    if (dh > MAXH) { dh = MAXH; dw = Math.round(MAXH * w / h); }
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 240, after: 240, line: 240, lineRule: LineRuleType.AUTO },
      children: [new ImageRun({
        type: 'png',
        data: fs.readFileSync(file),
        transformation: { width: dw, height: dh },
      })],
    }));
    i++; continue;
  }

  // headings
  if (/^#### /.test(t)) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_4,
      spacing: { before: 200, after: 100 },
      children: [new TextRun({ text: t.replace(/^#### /, ''), font: HEI, size: 24, bold: true, italics: false, color: '333333' })],
    }));
    i++; continue;
  }
  if (/^### /.test(t)) {
    tocEntries.push({ level: 2, text: t.replace(/^### /, '') });
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_3,
      spacing: { before: 260, after: 120 },
      children: [new TextRun({ text: t.replace(/^### /, ''), font: HEI, size: 26, bold: true, italics: false, color: NAVY })],
    }));
    i++; continue;
  }
  if (/^## /.test(t)) {
    const title = t.replace(/^## /, '');
    const isChapter = /^第.+章/.test(title) || ['方案摘要', '结语', '附录'].some(k => title.startsWith(k));
    if (isChapter && !firstChapter) children.push(new Paragraph({ children: [new PageBreak()] }));
    firstChapter = false;
    tocEntries.push({ level: 1, text: title });
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      spacing: { before: 240, after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: RED, space: 6 } },
      children: [new TextRun({ text: title, font: HEI, size: 32, bold: true, italics: false, color: NAVY })],
    }));
    i++; continue;
  }

  // table
  if (/^\|/.test(t)) {
    const block = [];
    while (i < raw.length && /^\s*\|/.test(raw[i])) { block.push(raw[i]); i++; }
    flushTable(block);
    continue;
  }

  // code fence
  if (/^```/.test(t)) {
    i++;
    const code = [];
    while (i < raw.length && !/^```/.test(raw[i].trim())) { code.push(raw[i]); i++; }
    i++;
    code.forEach(cl => children.push(new Paragraph({
      shading: { type: ShadingType.CLEAR, fill: 'F5F6F8', color: 'auto' },
      spacing: { line: 260, before: 0, after: 0 },
      indent: { left: 260 },
      children: [new TextRun({ text: cl.replace(/\t/g, '    ') || ' ', font: MONO, size: 19 })],
    })));
    children.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: '', size: 12 })] }));
    continue;
  }

  // blockquote
  if (/^> /.test(t) || t === '>') {
    const q = [];
    while (i < raw.length && /^\s*>/.test(raw[i])) { q.push(raw[i].trim().replace(/^>\s?/, '')); i++; }
    q.filter(x => x !== '').forEach(qt => children.push(new Paragraph({
      shading: { type: ShadingType.CLEAR, fill: 'F7F3E8', color: 'auto' },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: 'C9A227', space: 8 } },
      indent: { left: 300, right: 200 },
      spacing: { line: 360, before: 80, after: 80 },
      children: runs(qt, { font: KAI, size: 24 }),
    })));
    children.push(new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: '', size: 12 })] }));
    continue;
  }

  // bullet list
  if (/^- /.test(t)) {
    children.push(new Paragraph({
      numbering: { reference: 'hz-bullet', level: 0 },
      spacing: { line: 360, before: 40, after: 40 },
      alignment: AlignmentType.JUSTIFIED,
      children: runs(t.replace(/^- /, '')),
    }));
    i++; continue;
  }

  // ordered list
  if (/^\d+\.\s/.test(t)) {
    if (Number(t.match(/^(\d+)\./)[1]) === 1) numInstance++;
    children.push(new Paragraph({
      numbering: { reference: 'hz-num', level: 0, instance: numInstance },
      spacing: { line: 360, before: 40, after: 40 },
      alignment: AlignmentType.JUSTIFIED,
      children: runs(t.replace(/^\d+\.\s/, '')),
    }));
    i++; continue;
  }

  // italic-only trailing note
  if (/^\*[^*].*\*$/.test(t)) {
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      spacing: { line: 360, before: 200 },
      children: [new TextRun({ text: t.replace(/^\*|\*$/g, ''), font: KAI, size: 22, italics: false, color: '555555' })],
    }));
    i++; continue;
  }

  // plain paragraph
  children.push(body(t));
  i++;
}

// ===== Static TOC with dot leaders =====
const tocParas = tocEntries.map(e => new Paragraph({
  spacing: { line: 300, before: e.level === 1 ? 110 : 20, after: 20 },
  indent: { left: e.level === 1 ? 0 : 420, right: 60 },
  tabStops: [{ type: TabStopType.RIGHT, position: 9000, leader: LeaderType.DOT }],
  children: [
    new TextRun({
      text: e.text,
      font: e.level === 1 ? HEI : SONG,
      size: e.level === 1 ? 23 : 21,
      bold: e.level === 1,
      color: e.level === 1 ? NAVY : '333333',
    }),
    new TextRun({
      children: [new Tab(), String(PAGEMAP[e.text] || 0)],
      font: SONG, size: e.level === 1 ? 23 : 21, color: '555555',
    }),
  ],
}));
children.splice(tocInsertAt, 0, ...tocParas);
fs.writeFileSync(path.join(__dirname, 'toc_headings.json'), JSON.stringify(tocEntries, null, 1));

// ===== Document =====
const doc = new Document({
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: SONG, size: 24 }, paragraph: { spacing: { line: 380 } } },
    },
  },
  numbering: {
    config: [
      {
        reference: 'hz-bullet',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '●', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 300 } }, run: { color: RED, size: 18 } },
        }],
      },
      {
        reference: 'hz-num',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: { color: NAVY, bold: true } },
        }],
      },
    ],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: {
        size: { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
        margin: {
          top: convertMillimetersToTwip(25), bottom: convertMillimetersToTwip(25),
          left: convertMillimetersToTwip(28), right: convertMillimetersToTwip(28),
        },
      },
    },
    headers: {
      first: new Header({ children: [new Paragraph({ children: [new TextRun({ text: '' })] })] }),
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '9AA6BC', space: 4 } },
          children: [new TextRun({ text: '嘉兴大学「禾章」中国特色高质量教材体系研究智能体框架设计方案', font: HEI, size: 18, color: '667085' })],
        })],
      }),
    },
    footers: {
      first: new Footer({ children: [new Paragraph({ children: [new TextRun({ text: '' })] })] }),
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: ['— ', PageNumber.CURRENT, ' —'], font: SONG, size: 20, color: '667085' })],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(OUT, b);
  console.log('wrote', OUT, (b.length / 1024 / 1024).toFixed(2) + 'MB', '| blocks:', children.length);
});
