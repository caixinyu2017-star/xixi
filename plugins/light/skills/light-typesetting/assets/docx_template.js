/**
 * docx_template.js — 用 docx-js (npm 包 "docx") 以代码构造 Word 文档的完整模板。
 *
 * 安装:  npm install docx
 * 运行:  node docx_template.js   ->  生成 output.docx
 *
 * 覆盖: Document/Packer 样板、DXA 尺寸换算表、Heading 样式 + outlineLevel(决定导航窗格/TOC层级)、
 *       TableOfContents 字段、页眉/页脚 + 页码、A4 vs US Letter 显式页面设置、三线表、题注段落。
 *
 * 关键单位: docx 内部长度单位是 DXA (twips), 1 inch = 1440 dxa, 1 pt = 20 dxa, 1 cm ≈ 567 dxa。
 * 字号 size 用半磅 (half-points): 12pt -> size:24。
 */
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  PageNumber, Header, Footer, TableOfContents, Table, TableRow, TableCell,
  BorderStyle, WidthType, LevelFormat, convertInchesToTwip, convertMillimetersToTwip,
} = require("docx");
const fs = require("fs");

// --- DXA 尺寸换算表 (常用值, 便于直接套) -------------------------------
const DXA = {
  inch: 1440,            // 1 in
  pt: 20,                // 1 pt
  cm: 567,               // 1 cm (≈)
  mm: 56.7,              // 1 mm (≈)
  // 页面 (纵向)
  A4: { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
  LETTER: { width: convertInchesToTwip(8.5), height: convertInchesToTwip(11) },
  // 常见页边距
  margin1in: convertInchesToTwip(1),     // 1 英寸 = 1440
  margin2_54cm: convertMillimetersToTwip(25.4),
};

// 切换纸张: 改这一行即可在 A4 / US Letter 间切换
const PAGE = DXA.A4;            // 或 DXA.LETTER

// --- 三线表 (booktabs 风格: 仅顶/中/底横线) ----------------------------
// (删除原 topBottom(width) 的死参 width——它从未被使用)
function topBottom() {
  return { top: { style: BorderStyle.SINGLE, size: 8, color: "000000" },
           bottom: { style: BorderStyle.SINGLE, size: 8, color: "000000" },
           left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } };
}
function makeTriLineTable() {
  const headerCells = ["Method", "Metric A", "Metric B"].map((t, i) =>
    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: t, bold: true })] })],
      borders: topBottom(), width: { size: 33, type: WidthType.PERCENTAGE } }));
  const dataRows = [["Baseline", "0.80", "0.75"], ["Ours", "0.88", "0.83"]].map((row, ri) =>
    new TableRow({ children: row.map((c) => new TableCell({
      children: [new Paragraph(c)],
      borders: ri === 1 ? { bottom: { style: BorderStyle.SINGLE, size: 8, color: "000000" },
        top: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }
        : { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
            left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } } })) }));
  // 表头下加一条中线
  const headerRow = new TableRow({ children: headerCells.map((c) => c), tableHeader: true });
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: [headerRow, ...dataRows] });
}

// --- 文档构造 ---------------------------------------------------------
const doc = new Document({
  creator: "light-typesetting",
  title: "Sample Document",
  // 自定义样式: 覆盖标题字体/字号, 并通过 outlineLevel 决定大纲层级(导航窗格/TOC)
  styles: {
    // 默认字体: 西文 Times New Roman + 中文 eastAsia 宋体, 中英混排不回退默认字体(修无 CJK 字体)
    default: {
      document: {
        run: { font: { ascii: "Times New Roman", hAnsi: "Times New Roman", eastAsia: "SimSun" }, size: 24 },
      },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "2E2E2E", font: { eastAsia: "SimHei" } },
        paragraph: { outlineLevel: 0, spacing: { before: 240, after: 120 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: { eastAsia: "SimHei" } },
        paragraph: { outlineLevel: 1, spacing: { before: 200, after: 100 } } },
      { id: "Caption", name: "Caption", basedOn: "Normal", next: "Normal",
        run: { size: 18, italics: true }, paragraph: { spacing: { before: 60, after: 120 } } },
    ],
  },
  // 真·多级列表(LevelFormat 自动连号), 替代手敲 "1./1.1"; 引用处用 reference:"multilevel"
  numbering: {
    config: [{
      reference: "multilevel",
      levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START,
          style: { paragraph: { indent: { left: 360, hanging: 360 } } } },
        { level: 1, format: LevelFormat.DECIMAL, text: "%1.%2", alignment: AlignmentType.START,
          style: { paragraph: { indent: { left: 720, hanging: 432 } } } },
        { level: 2, format: LevelFormat.LOWER_LETTER, text: "(%3)", alignment: AlignmentType.START,
          style: { paragraph: { indent: { left: 1080, hanging: 432 } } } },
      ],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE.width, height: PAGE.height },   // A4 vs Letter 显式设置
        margin: { top: DXA.margin1in, bottom: DXA.margin1in,
                  left: DXA.margin1in, right: DXA.margin1in },
      },
    },
    // 页眉
    headers: { default: new Header({ children: [
      new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "Paper Title — Running Head", size: 18, color: "808080" })] }) ] }) },
    // 页脚: "Page X of Y"
    footers: { default: new Footer({ children: [
      new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ children: ["Page ", PageNumber.CURRENT, " of ", PageNumber.TOTAL_PAGES], size: 18 }) ] }) ] }) },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Document Title", bold: true, size: 40 })] }),
      // 目录: Word 打开后右键 "更新域" 才会填充页码
      new Paragraph({ text: "Table of Contents", heading: HeadingLevel.HEADING_1 }),
      new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-3" }),
      new Paragraph({ text: "1. Introduction", heading: HeadingLevel.HEADING_1 }),
      new Paragraph("正文段落。这是引言部分。"),
      new Paragraph({ text: "1.1 Background", heading: HeadingLevel.HEADING_2 }),
      new Paragraph("二级标题下的内容。"),
      new Paragraph({ text: "2. Method", heading: HeadingLevel.HEADING_1 }),
      // 真·多级列表: 用 numbering reference + level 自动连号(替手敲 "1./1.1/(a)"),
      // 增删条目自动重排, 不会出现手敲编号漏改的错乱
      new Paragraph({ text: "方法分三步:", spacing: { before: 80 } }),
      new Paragraph({ numbering: { reference: "multilevel", level: 0 }, children: [new TextRun("数据预处理")] }),
      new Paragraph({ numbering: { reference: "multilevel", level: 1 }, children: [new TextRun("清洗与去重")] }),
      new Paragraph({ numbering: { reference: "multilevel", level: 1 }, children: [new TextRun("划分训练/验证集")] }),
      new Paragraph({ numbering: { reference: "multilevel", level: 0 }, children: [new TextRun("模型训练(中英混排示例: training with 对比学习)")] }),
      new Paragraph({ numbering: { reference: "multilevel", level: 2 }, children: [new TextRun("超参网格搜索")] }),
      makeTriLineTable(),
      new Paragraph({ text: "Table 1. 实验结果对比 (三线表).", style: "Caption" }),
      new Paragraph({ text: "3. Conclusion", heading: HeadingLevel.HEADING_1 }),
      new Paragraph("总结段落。"),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = "output.docx";
  fs.writeFileSync(out, buf);
  console.log("wrote " + out + " (" + buf.length + " bytes)");
});
