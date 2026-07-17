// .vitepress/config.ts
import { defineConfig } from "vitepress";
import llmstxt from "vitepress-plugin-llms";
import { teekConfig } from "./teekConfig";

const description = "深深别院，潜潜牧志，一个 Python 开发者的个人wiki。之前主要研究代码，现在主要研究投资理财。";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  extends: teekConfig,
  title: "别院牧志知识库",
  description: description,
  cleanUrls: true, 
  lastUpdated: true,
  lang: "zh-CN",

  // Head 配置 (SEO & 统计)
  head: [
    ["link", { rel: "icon", href: "/img/favicon.ico" }],
    ["meta", { name: "keywords", content: "别院牧志, imoyao, idealyard, 张牧志, 牧志, Python, 编程, Python开发, 投资理财" }],
    ["meta", { name: "baidu-site-verification", content: "code-17W2qEmqf4" }],
    ["meta", { name: "theme-color", content: "#11a8cd" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:locale", content: "zh-CN" }],
    ["meta", { property: "og:title", content: "别院牧志知识库" }],
    ["meta", { property: "og:site_name", content: "别院牧志" }],
    ["meta", { property: "og:description", content: description }],
    ["meta", { property: "og:url", content: "https://wiki.masantu.com" }],
  ],

  // Markdown 配置
  markdown: {
    lineNumbers: true,
    image: { lazyLoading: true },
    math: true, // 启用数学公式
    
    // ✅ 保留 VitePress 原生内置容器的中文标签配置 (tip, warning, danger, info 等)
    container: {
      tipLabel: "提示",
      warningLabel: "警告",
      dangerLabel: "危险",
      infoLabel: "信息",
      detailsLabel: "详细信息",
    },
    
    // ✅ 保留你的防 Vue 编译器解析 HTML 块中 {{ }} 的逻辑
    // 注意：这里只是修改 renderer rules，不是 md.use()，所以放在 config.ts 是安全的！
    config: (md) => {
      const originalHtmlBlock = md.renderer.rules.html_block;
      md.renderer.rules.html_block = (tokens, idx, options, env, self) => {
        const content = tokens[idx].content;
        return `<pre v-pre>${content}</pre>`;
      };
      
      const originalHtmlInline = md.renderer.rules.html_inline;
      md.renderer.rules.html_inline = (tokens, idx, options, env, self) => {
        const content = tokens[idx].content;
        // @ts-ignore
        if (content.includes("{{") || content.includes("{%")) {
          return `<span v-pre>${content}</span>`;
        }
        return originalHtmlInline
          ? originalHtmlInline(tokens, idx, options, env, self)
          : self.renderToken(tokens, idx, options);
      };
    },
  },

  // Sitemap 配置
  sitemap: {
    hostname: "https://wiki.masantu.com",
    transformItems: (items) => {
      const permalinkItemBak: typeof items = [];
      const permalinks = (globalThis as any).VITEPRESS_CONFIG?.site?.themeConfig?.permalinks;
      if (permalinks?.map) {
        items.forEach((item) => {
          const permalink = permalinks.map[item.url];
          if (permalink) permalinkItemBak.push({ url: permalink, lastmod: item.lastmod });
        });
      }
      return [...items, ...permalinkItemBak];
    },
  },

  // 主题配置
  themeConfig: {
    logo: "/img/vertical-logo.png",
    darkModeSwitchLabel: "主题",
    sidebarMenuLabel: "菜单",
    returnToTopLabel: "返回顶部",
    lastUpdatedText: "上次更新时间",
    outline: {
      level: [2, 3],
      label: "本页导航",
    },
    docFooter: {
      prev: "上一页",
      next: "下一页",
    },

    nav: [
      { text: "首页", link: "/" },
      {
        text: "Python",
        link: "/python/",
        items: [
          { text: "基础", items: [{ text: "全栈之路", link: "/python/fullstack/index/" }, { text: "😎Awesome资源", link: "/python/awesome/" }] },
          { text: "进阶", items: [{ text: "Python 工匠系列", link: "/pythonista/index/" }, { text: "高阶知识点", link: "/python/GIL/" }] },
          { text: "指南教程", items: [{ text: "Socket 编程", link: "/socket/index/" }, { text: "异步编程", link: "/python/async/index/" }, { text: "PEP 系列", link: "/peps/index/" }] },
        ],
      },
      {
        text: "面试",
        items: [
          { text: "Python 面试题", link: "/python/interview/" },
          { text: "2025 面试记录", link: "/interview-2025/" },
          { text: "2022 面试记录", link: "/interview-2022/" },
          { text: "2021 面试记录", link: "/interview-2021/" },
          { text: "2020 面试记录", link: "/interview-2020/" },
          { text: "2019 面试记录", link: "/interview-2019/" },
          { text: "数据库索引原理", link: "/mysql/mysql-index/" },
        ],
      },
      {
        text: "理财",
        link: "/finance/",
        items: [
          { text: "基金知识", link: "/funds/04a189/" },
          { text: "基金经理", link: "/fund-managers/" },
          { text: "德隆-三个知道", link: "/invest/3-knows/" },
          { text: "孔曼子-摊大饼理论", link: "/invest/decentralize/" },
          { text: "配置者说-躺赢之路", link: "/invest/road-to-win/" },
          { text: "资水-建立自己的投资体系", link: "/invest/create-your-invest-system/" },
          { text: "反脆弱", link: "/invest/antifragile/" },
        ],
      },
      { text: "其他", items: [{ text: "Git 参考手册", link: "/git/reference/" }, { text: "提问的智慧", link: "/smart-questions/" }] },
      { text: "索引", link: "/archives/", items: [{ text: "分类", link: "/categories/" }, { text: "标签", link: "/tags/" }, { text: "归档", link: "/archives/" }] },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/imoyao/wiki" },
    ],

    search: {
      provider: "local",
      options: {
        detailedView: true,
      },
    },

    editLink: {
      text: "在 GitHub 上编辑此页",
      pattern: "https://github.com/imoyao/wiki/edit/master/docs/:path",
    },
  },

  // Vite 插件
  vite: {
    plugins: [llmstxt() as any],
  },
});