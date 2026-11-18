#!/usr/bin/env node
/**
 * 从 VitePress 项目的 frontmatter permalink 生成 Cloudflare Pages 的 `_redirects`。
 *
 * 背景：VitePress 的 `cleanUrls: true` 让产物文件是 xxx.html，而 frontmatter 的
 * permalink 是 /xxx —— 两者不一致。permalink 插件在 dev 下靠中间件重写、在生产下
 * 靠改写默认主题 Layout 注入客户端路由来兜底；静态托管（Pages/Workers Assets）
 * 两样都没有，直接访问 permalink 就 404。本脚本在构建期把映射固化成服务端重写规则。
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

import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from 'node:fs'
import { resolve, dirname, join, relative, basename } from 'node:path'
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
  }
}

const cfg = detectConfig()
const docsDir = resolve(repoRoot, getArg('docs', cfg.srcDir))
const outFile = resolve(repoRoot, getArg('out', join(docsDir, '.vitepress/dist/_redirects')))
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
  // frontmatter 必须从文件第一行 --- 开始
  if (!/^---\s*\r?\n/.test(text)) return null
  const end = text.indexOf('\n---', 3)
  if (end < 0) return null
  const fm = text.slice(3, end)
  for (const line of fm.split(/\r?\n/)) {
    const m = line.match(/^\s*permalink\s*:\s*(.+?)\s*$/)
    if (!m) continue
    let v = m[1].trim()
    // 去引号
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1)
    }
    // 去行内注释与查询串
    v = v.split(/\s+#/)[0].split('?')[0].trim()
    return v || null
  }
  return null
}

/**
 * 把源 md 路径换算成产物的物理文件路径。
 * 注意：cleanUrls 只影响「链接长什么样」，不影响产物文件名 —— VitePress 始终
 * 生成 .html 文件。_redirects 是服务端重写，目标必须写物理路径。
 *   index.md              -> /index.html
 *   @pages/archivesPage.md -> /@pages/archivesPage.html
 *   foo/index.md          -> /foo/index.html
 *
 * _redirects 每行按空白切成 [source, destination, code] 三段，路径里的空格会
 * 破坏解析，因此逐段做 percent-encoding（保留 / 与非 ASCII，避免双重编码）。
 */
function sourceToUrl(relPath) {
  const p = relPath.replace(/\\/g, '/').replace(/\.md$/i, '')
  const encoded = p
    .split('/')
    .map((seg) => seg.replace(/[ !()]/g, (ch) => encodeURIComponent(ch)))
    .join('/')
  return '/' + encoded + '.html'
}

// ---------- 生成规则 ----------
const files = walk(docsDir)
const rules = []
const seen = new Map()
let skipped = 0

for (const file of files) {
  const permalink = readPermalink(file)
  if (!permalink) continue
  if (!permalink.startsWith('/')) {
    skipped++
    console.warn(`[permalink-redirects] 跳过非绝对路径 permalink: ${permalink} (${relative(repoRoot, file)})`)
    continue
  }
  const dest = sourceToUrl(relative(docsDir, file))

  // 规范化 permalink：去尾部斜杠（根路径除外），避免 /archives 与 /archives/ 重复
  const norm = permalink.length > 1 ? permalink.replace(/\/+$/, '') : permalink

  if (seen.has(norm) && seen.get(norm) !== dest) {
    skipped++
    console.warn(`[permalink-redirects] permalink 冲突: ${norm} -> ${seen.get(norm)} / ${dest}（保留前者）`)
    continue
  }
  seen.set(norm, dest)
  rules.push({ permalink: norm, dest, source: relative(repoRoot, file) })
}

rules.sort((a, b) => a.permalink.localeCompare(b.permalink))

const lines = [
  '# 由 scripts/generate-permalink-redirects.mjs 自动生成，请勿手工编辑。',
  `# 源: ${relative(repoRoot, cfg.file || '约定配置')} | srcDir: ${relative(repoRoot, docsDir)} | cleanUrls: ${cfg.cleanUrls}`,
  `# 共 ${rules.length} 条，跳过 ${skipped} 条。`,
  '',
  ...rules.map((r) => `${r.permalink} ${r.dest} ${code}`),
  '',
]

const content = lines.join('\n')

if (dryRun) {
  console.log(content)
} else {
  writeFileSync(outFile, content, 'utf-8')
  console.log(`[permalink-redirects] 已写入 ${relative(repoRoot, outFile)}（${rules.length} 条，跳过 ${skipped} 条）`)
}
