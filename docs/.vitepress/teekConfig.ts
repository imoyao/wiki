// .vitepress/teekConfig.ts
import { defineTeekConfig } from "vitepress-theme-teek/config";
import { version } from "vitepress-theme-teek/es/version";

export const teekConfig = defineTeekConfig({
  // 使用 VitePress 默认首页风格（features 卡片）
  teekHome: false,
  vpHome: true,

  // 基础功能
  sidebarTrigger: true,
  loading: false,

  // 作者信息
  author: {
    name: "佚名",
    link: "https://github.com/imoyao",
  },

  // 全站背景图片（轮播）
  bodyBgImg: {
    imgSrc: [
      "https://cdn.jsdelivr.net/gh/xugaoyi/image_store/blog/20200507175828.jpeg",
      "https://cdn.jsdelivr.net/gh/xugaoyi/image_store/blog/20200507175845.jpeg",
      "https://cdn.jsdelivr.net/gh/xugaoyi/image_store/blog/20200507175846.jpeg",
    ],
    opacity: 0.5,
  },

  // 社交图标 (迁移自 vdoing)
  social: [
    { icon: "icon-youjian", name: "发邮件", link: "mailto:immoyao@gmail.com" },
    { icon: "icon-github", name: "GitHub", link: "https://github.com/imoyao/wiki" },
    { icon: "icon-bokeyuan", name: "博客", link: "https://www.masantu.com" },
    { icon: "icon-juejin", name: "旧版", link: "https://vk.masantu.com" },
  ],

  // 页脚信息 (迁移自 vdoing)
  footerInfo: {
    copyright: {
      createYear: 2019,
      suffix: "IMOYAO | 别院牧志",
    },
    license: "MIT License",
  },

  // 文章信息分析（字数、阅读时长）
  articleAnalyze: { enabled: true },
  // 面包屑导航
  breadcrumb: { enabled: true },
  // 最近更新栏
  articleUpdate: {
    enabled: true,
    moreArticle: "/archives/",
  },

  // 评论系统 - Twikoo
  comment: {
    provider: "twikoo",
    options: {
      envId: "https://twikoo.masantu.com/",
    },
  },
  
  codeBlock: {
    copiedDone: (TkMessage) => TkMessage.success("复制成功！"),
  },
  
  articleShare: { enabled: true },

  // 站点分析 - 百度统计
  siteAnalytics: [
    {
      provider: "baidu",
      options: {
        id: "d21148b4e4af8bc78f02e77d0fd45ec0",
      },
    },
  ],

  // ==========================================
  // ✅ Vite 插件配置 (严格按照官方文档的布尔值+Option结构)
  // ==========================================
  vitePlugins: {
    sidebar: true, 
    sidebarOption: {
      // 自动侧边栏生成（对应 vdoing 的 sidebar: 'structuring'）
      // 排除不需要生成侧边栏的目录
      exclude: ['/guide/', '/reference/', '/develop/']
    }, 
    
    permalink: true, 
    permalinkOption: {
      // 🔥 永久链接：使用 rewrite 模式保证旧链接不失效，且避免 duplicate ID
      mode: 'rewrite', 
    },
    
    mdH1: false, // 自动 h1 标题 (关闭)
    
    catalogue: true, // 目录页 (开启)
    catalogueOption: {}, 
    
    docAnalysis: true, // 文档分析 (开启)
    docAnalysisOption: {}, 
    
    fileContentLoaderIgnore: [], // 文件内容加载器忽略路径
    
    autoFrontmatter: true, // 自动生成 frontmatter
    autoFrontmatterOption: {
      permalinkPrefix: "pages",
      categories: true,
    },
  },

  // ==========================================
  // ✅ Markdown 配置 (容器、自定义插件必须放在这里！)
  // ==========================================
  markdown: {
    // 注意：如果你以后有真实的 markdown-it 插件要引入，再在这里写 config: (md) => { md.use(真实插件) }

    // 容器配置
    container: {
      // 修改 Teek 内置容器的默认标题
      label: {
        noteLabel: "笔记", // 修改 ::: note 的默认标题
      },
      
      // 自定义全新的 Markdown 容器
      config: () => [
        // 示例：创建一个带标题的自定义容器
        { 
          type: "thought", 
          useTitle: true, 
          defaultTitle: "随想", 
          className: "thought-container" 
        },
        // 示例：创建一个不带标题的自定义容器
        { 
          type: "highlight", 
          useTitle: false, 
          className: "highlight-container" 
        },
      ],
    },

    // 3. Demo 容器配置 (如果你需要用到 ::: demo)
    demo: {
      disabled: false,
      playgroundUrl: "",
      githubUrl: "https://github.com/imoyao/wiki",
    }
  },
});