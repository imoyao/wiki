#!/usr/bin/env node
/**
 * 从 VitePress 项目的 frontmatter permalink 生成 Cloudflare Pages 的 `_redirects`。
 *
 * ── 关键约束（2026-11-18 修正）─────────────────────────────────────────────
 * Cloudflare Pages 会把任何 /foo.html 形式的 URL 308 规范化为 /foo。因此本脚本
 * 生成的规则目标【绝不能写 .html】—— 否则会形成死循环：
 *     /foo -> /foo.html (_redirects 200 重写) -> /foo (Pages 308) -> ... 无限循环
 *
 * 启用 A 方案（teek createRewrites）后，permalink 的物理 .html 已真实存在，
 * Pages 自身就会把 clean URL /foo 映射到 foo.html（与 / 映射到 index.html 同理），
 * 无需任何规则。本脚本只为「permalink 物理文件不存在」的少数页面生成规则：
 * 典型是文件名含空格导致 createRewrites 失效的页面，此时规则目标写源文件的
 * clean 路径（不带 .html），由 Pages 自动映射到源 .html。
 *
 * 通用性：不写死任何项目路径或 permalink 列表，扫描任意 VitePress 项目的 docs 目录。
 * 通过 VitePress 配置文件读取 srcDir / cleanUrls / base，未读到时回退到约定值。
 *
 * 用法：node scripts/generate-permalink-redirects.mjs [options]
 *   --docs <dir>   文档根目录，默认从 vitepress config 探测，探测失败用 docs
 *   --out <file>   输出文件，默认 <docs>/.vitepress/dist/_redirects
 *   --code <n>     状态码，默认 200（内部重写，URL 不变）
 *   --dry-run      只打印规则，不写文件
 */

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve, dirname, join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const repoRoot = resolve(__dirname, '..')

// ---------- 参数 ----------
const argv = process.argv.slice(2)
const getArg = (name, fallback) => {
  const i = argv.indexOf(`--${name}`)
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback
}
const hasFlag = (name) => argv.includes(`--${name}`)

// ---------- 探测 VitePress 配置（纯文本，避免 TS 编译依赖） ----------
function detectConfig() {
  const candidates = [
    join(repoRoot, 'docs/.vitepress/config.ts'),
    join(repoRoot, 'docs/.vitepress/config.mts'),
    join(repoRoot, 'docs/.vitepress/config.js'),
    join(repoRoot, 'docs/.vitepress/config.mjs'),
  ]
  const file = candidates.find(existsSync)
  if (!file) return { file: null, srcDir: 'docs', cleanUrls: false, base: '/' }

  const text = readFileSync(file, 'utf-8')
  const pick = (key, fallback) => {
    const m = text.match(new RegExp(`\\b${key}\\s*:\\s*(true|false|['"]([^'"]*)['"])`))
    if (!m) return fallback
    if (m[1] === 'true') return true
    if (m[1] === 'false') return false
    return m[2]
  }
  return {
    file,
    srcDir: pick('srcDir', 'docs'),
    cleanUrls: pick('cleanUrls', false) === true,
    base: pick('base', '/') || '/',
    rewritesHint: /\brewrites\s*:/.test(text) && /createRewrites/.test(text),
  }
}

const cfg = detectConfig()
const docsDir = resolve(repoRoot, getArg('docs', cfg.srcDir))
const outFile = resolve(repoRoot, getArg('out', join(docsDir, '.vitepress/dist/_redirects')))
const distDir = dirname(outFile)
const code = getArg('code', '200')
const dryRun = hasFlag('dry-run')

if (!existsSync(docsDir)) {
  console.error(`[permalink-redirects] 文档目录不存在: ${docsDir}`)
  process.exit(1)
}

// ---------- 扫描 markdown ----------
const SKIP_DIRS = new Set(['node_modules', '.git', '.vitepress', 'public', 'dist'])

function walk(dir) {
  const out = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue
      out.push(...walk(join(dir, entry.name)))
    } else if (/\.md$/i.test(entry.name)) {
      out.push(join(dir, entry.name))
    }
  }
  return out
}

/** 读取 frontmatter 中的 permalink 字段（支持引号、行内注释）。 */
function readPermalink(file) {
  const text = readFileSync(file, 'utf-8')
  if (!/^---\s*\r?\n/.test(text)) return null
  const end = text.indexOf('\n---', 3)
  if (end < 0) return null
  const fm = text.slice(3, end)
  for (const line of fm.split(/\r?\n/)) {
    const m = line.match(/^\s*permalink\s*:\s*(.+?)\s*$/)
    if (!m) continue
    let v = m[1].trim()
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1)
    }
    v = v.split(/\s+#/)[0].split('?')[0].trim()
    return v || null
  }
  return null
}

/**
 * _redirects 每行按空白切成 [source, destination, code] 三段，路径里的空格会
 * 破坏解析，因此逐段做 percent-encoding（只编码空白与括号，保留 / 与非 ASCII）。
 */
function encodePath(p) {
  return p
    .split('/')
    .map((seg) => seg.replace(/[ !()]/g, (ch) => encodeURIComponent(ch)))
    .join('/')
}

/** 清理成以 / 开头的 clean 路径（无尾斜杠、无 .html）。 */
function cleanPath(raw) {
  return '/' + raw.replace(/^\/+/, '').replace(/\/+$/, '')
}

/**
 * 判断是否需要生成重写规则，并给出目标（clean 路径，绝不带 .html）。
 *  - permalink 的物理 .html 已存在（A 方案成功）：Pages 自动映射 clean URL，无需规则。
 *  - 否则源文件 .html 仍在原位（A 覆盖不到）-> 规则目标 = 源的 clean 路径。
 *  - 两者都不存在（尚未 build）-> 回退到 permalink clean 路径并告警。
 */
function resolveDest(permalink, relPath) {
  const srcBase = cleanPath(relPath.replace(/\\/g, '/').replace(/\.md$/i, ''))
  const permalinkBase = permalink === '/' ? '/' : cleanPath(permalink)
  const srcHtml = srcBase === '/' ? '/index.html' : srcBase + '.html'
  const permalinkHtml = permalinkBase === '/' ? '/index.html' : permalinkBase + '.html'

  if (existsSync(join(distDir, permalinkHtml.replace(/^\/+/, '')))) {
    return { needRule: false, reason: 'auto' }
  }
  if (existsSync(join(distDir, srcHtml.replace(/^\/+/, '')))) {
    return { needRule: true, dest: encodePath(srcBase), reason: 'source' }
  }
  console.warn(`[permalink-redirects] 目标均不存在，回退到 permalink clean 路径: ${permalink} -> ${permalinkBase} (源 ${relPath})`)
  return { needRule: true, dest: encodePath(permalinkBase), reason: 'fallback' }
}

// ---------- 生成规则 ----------
const files = walk(docsDir)
const rules = []
const seen = new Map()
let skipped = 0
let autoCount = 0
let sourceCount = 0
let fallbackCount = 0

for (const file of files) {
  const permalink = readPermalink(file)
  if (!permalink) continue
  if (!permalink.startsWith('/')) {
    skipped++
    console.warn(`[permalink-redirects] 跳过非绝对路径 permalink: ${permalink} (${relative(repoRoot, file)})`)
    continue
  }
  const relPath = relative(docsDir, file)
  const r = resolveDest(permalink, relPath)
  if (!r.needRule) {
    autoCount++
    continue
  }
  if (r.reason === 'source') sourceCount++
  else fallbackCount++

  // 规范化 permalink：去尾部斜杠（根路径除外）
  const norm = permalink.length > 1 ? permalink.replace(/\/+$/, '') : permalink

  if (seen.has(norm) && seen.get(norm) !== r.dest) {
    skipped++
    console.warn(`[permalink-redirects] permalink 冲突: ${norm} -> ${seen.get(norm)} / ${r.dest}（保留前者）`)
    continue
  }
  seen.set(norm, r.dest)
  rules.push({ permalink: norm, dest: r.dest, source: relative(repoRoot, file) })
}

rules.sort((a, b) => a.permalink.localeCompare(b.permalink))

// 只生成无尾斜杠的 source：Pages 自身会把 /foo/ 308 规范化到 /foo，
// 额外生成 /foo/ 规则反而会在规范化前后制造混淆。目标一律是不带 .html 的 clean 路径。
const emit = rules.map((r) => `${r.permalink} ${r.dest} ${code}`)
if (emit.length > 2000) {
  console.warn(`[permalink-redirects] 规则数 ${emit.length} 超过 Cloudflare Pages 静态重定向上限 2000`)
}

const lines = [
  '# 由 scripts/generate-permalink-redirects.mjs 自动生成，请勿手工编辑。',
  '# 目标一律为 clean 路径（不带 .html）—— Pages 会把 /foo.html 308 到 /foo，规则写 .html 会造成循环。',
  `# 源: ${relative(repoRoot, cfg.file || '约定配置')} | srcDir: ${relative(repoRoot, docsDir)} | rewritesHint: ${cfg.rewritesHint}`,
  `# ${autoCount} 个 permalink 由 Pages 自动映射（无需规则）；${rules.length} 个需重写（源路径 ${sourceCount} / 回退 ${fallbackCount}），跳过 ${skipped} 条。`,
  '',
  ...emit,
  '',
]

const content = lines.join('\n')

if (dryRun) {
  console.log(content)
} else {
  writeFileSync(outFile, content, 'utf-8')
  console.log(`[permalink-redirects] 已写入 ${relative(repoRoot, outFile)}（${rules.length} 条规则；Pages 自动映射 ${autoCount} 条；源路径 ${sourceCount} / 回退 ${fallbackCount}；跳过 ${skipped} 条）`)
}
