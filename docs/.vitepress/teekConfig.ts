// .vitepress/teekConfig.ts
import { defineTeekConfig } from "vitepress-theme-teek/config";

export const teekConfig = defineTeekConfig({
  // 使用 VitePress 默认首页风格（features 卡片）
  teekHome: true,
  vpHome: false,

  // 基础功能
  sidebarTrigger: true,
  loading: true,
  homeCardListPosition: "right",
  anchorScroll: true,
  viewTransition: {
    enabled: true, // 是否启用深浅色切换动画效果
    mode: "out-in", // 动画模式，out 始终从点击点往全屏扩散，out-in 第一次从点击点往全屏扩散，再次点击从全屏回到点击点
    duration: 300, // 动画持续时间，当 mode 为 out 时，默认为 300ms，mode 为 out-in 时，默认为 600ms
    easing: "ease-in", // 缓动函数
  },
  backTop: {
    enabled: true, // 是否启动回到顶部功能
    content: "progress", // 回到顶部按钮的显示内容，可选配置 progress | icon
    done: TkMessage => TkMessage.success("返回顶部成功"), // 回到顶部后的回调
  },

  // 作者信息
  author: {
    name: "张牧志",
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

  // 页脚信息
  footerInfo: {
    copyright: {
      createYear: 2019,
      suffix: "IMOYAO | 别院牧志",
    },
    license: "MIT License",
  },

  // ==========================================
  // 📝 文章列表配置（核心：还原 Vdoing 的文章列表）
  // ==========================================
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
  
  // 代码块
  codeBlock: {
    enabled: true, // 是否启用新版代码块
    collapseHeight: 700, // 超出高度后自动折叠，设置 true 则默认折叠，false 则默认不折叠
    overlay: true, // 代码块底部是否显示展开/折叠遮罩层
    overlayHeight: 400, // 当出现遮罩层时，指定代码块显示高度，当 overlay 为 true 时生效
    langTextTransform: "lowercase", // 语言文本显示样式，为 text-transform 的值:none, capitalize, lowercase, uppercase
    copiedDone: (TkMessage) => TkMessage.success("复制成功！"),
  },

  // ==========================================
  // 🖼️ 首页 Banner 配置（还原 Vdoing 的大图 Banner）
  // ==========================================
  banner: {
    enabled: true, // 是否启用 Banner
    name: "别院牧志知识库", // Banner 标题，默认读取 vitepress 的 title 属性
    bgStyle: "fullImg", // Banner 背景风格：pure 为纯色背景，partImg 为局部图片背景，fullImg 为全屏图片背景
    pureBgColor: "#28282d", // Banner 背景色，bgStyle 为 pure 时生效
    imgSrc: ["/img/bg1.jpg", "/img/bg2.png"], // Banner 图片链接。bgStyle 为 partImg 或 fullImg 时生效
    imgInterval: 15000, // 当多张图片时（imgSrc 为数组），设置切换时间，单位：毫秒
    imgShuffle: true, // 图片是否随机切换，为 false 时按顺序切换，bgStyle 为 partImg 或 fullImg 时生效
    imgWaves: true, // 是否开启 Banner 图片波浪纹，bgStyle 为 fullImg 时生效
    mask: true, // Banner 图片遮罩，bgStyle 为 partImg 或 fullImg 时生效
    maskBg: "rgba(0, 0, 0, 0.3)", // Banner 遮罩颜色，如果为数字，则是 rgba(0, 0, 0, ${maskBg})，如果为字符串，则作为背景色。bgStyle 为 partImg 或 fullImg 且 mask 为 true 时生效
    textColor: "#ffffff", // Banner 字体颜色，bgStyle 为 pure 时为 '#000000'，其他为 '#ffffff'
    titleFontSize: "3.2rem", // 标题字体大小
    descFontSize: "1.4rem", // 描述字体大小
    descStyle: "types", // 描述信息风格：default 为纯文字渲染风格（如果 description 为数组，则取第一个），types 为文字打印风格，switch 为文字切换风格
    description: [
      "故事由我书写，旅程由你见证，传奇由她聆听",
      "积跬步以至千里，致敬每个爱学习的你",
      "投资理财 · Python开发 · 生活记录",
    ], // 描述信息
    switchTime: 4000, // 描述信息切换间隔时间，单位：毫秒。descStyle 为 switch 时生效
    switchShuffle: false, // 描述信息是否随机切换，为 false 时按顺序切换。descStyle 为 switch 时生效
    typesInTime: 150, // 输出一个文字的时间，单位：毫秒。descStyle 为 types 时生效
    typesOutTime: 80, // 删除一个文字的时间，单位：毫秒。descStyle 为 types 时生效
    typesNextTime: 800, // 打字与删字的间隔时间，单位：毫秒。descStyle 为 types 时生效
    typesShuffle: false, // 描述信息是否随机打字，为 false 时按顺序打字，descStyle 为 types 时生效
    features: [{ title: "", details: "", link: "", image: "" }], // 描述信息是否随机打字，为 false 时按顺序打字，descStyle 为 types 时生效
    featureCarousel: 4000, // feature 轮播间隔时间，单位：毫秒。仅在移动端生效（屏幕小于 719px）
  },
  // 壁纸模式，在首页 最顶部 进入全屏后开启，仅当 banner.bgStyle = 'fullImg' 或 bodyBgImg.imgSrc 存在才生效。
  wallpaper: {
    enabled: false, // 是否启用壁纸模式
    hideBanner: false, // 开启壁纸模式后，是否隐藏 Banner
    hideMask: false, // 开启壁纸模式后，是否隐藏 Banner 或 bodyBgImage 的遮罩层，则确保 banner.mask 和 bodyBgImage.mask 为 true 才生效
  },
  // 文章配置
  post: {
    postStyle: "list", // 文章列表风格
    excerptPosition: "top", // 文章摘要位置
    showMore: true, // 是否显示更多按钮
    moreLabel: "阅读全文 >", // 更多按钮文字
    emptyLabel: "暂无文章", // 文章列表为空时的标签
    coverImgMode: "small", // 文章封面图模式
    showCapture: true, // 是否在摘要位置显示文章部分文字，当为 true 且不使用 frontmatter.describe 和 <!-- more --> 时，会自动截取前 300 个字符作为摘要
    splitSeparator: true, // 文章信息（作者、创建时间、分类、标签等信息）是否添加 | 分隔符
    transition: true, // 是否开启过渡动画
    transitionName: "tk-slide-fade", // 自定义过渡动画名称
    listStyleTitleTagPosition: "right", // 列表模式下的标题标签位置（postStyle 为 list）
    cardStyleTitleTagPosition: "left", // 卡片模式下的标题标签位置（postStyle 为 card）
    defaultCoverImg: [], // 默认封面图地址，如果不设置封面图则使用默认封面图地址
  },
  page: {
    disabled: false, // 是否禁用
    pageSize: 10, // 每页显示条目数
    pagerCount: 7, // 设置最大页码按钮数。 页码按钮的数量，当总页数超过该值时会折叠
    layout: "prev, pager, next, jumper, ->, total", // 组件布局，子组件名用逗号分隔
    size: "default", // 分页大小
    background: false, // 是否为分页按钮添加背景色
    hideOnSinglePage: false, // 只有一页时是否隐藏
  },

  // ==========================================
  // 🗂️ 首页右侧卡片排序（还原 Vdoing 的侧边卡片）
  // ==========================================
  homeCardSort: [
    "topArticle",    // 精选文章
    "category",      // 分类
    "tag",           // 标签
    "friendLink",    // 友链
    "docAnalysis",   // 站点分析
  ],

  // 精选文章卡片
  topArticle: {
    enabled: true, // 是否启用精选文章卡片
    title: '<i class="i-mdi-fire" style="color: #ff9800; margin-right: 6px;"></i>精选文章',
    emptyLabel: "暂无精选文章", // 精选文章为空时的标签
    limit: 5, // 一页显示的数量
    autoPage: true, // 是否自动翻页
    pageSpeed: 4000, // 翻页间隔时间，单位：毫秒。autoPage 为 true 时生效
    dateFormat: "yyyy-MM-dd hh:mm:ss", // 精选文章的日期格式
    dateUTC: true, // 是否使用 UTC 时间
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
  // 分类卡片配置
  category: {
    enabled: true, // 是否启用分类卡片
    path: "/categories", // 分类页访问地址
    pageTitle: '<i class="i-mdi-folder-multiple-outline" style="color: #2196f3; margin-right: 6px;"></i>全部分类',
    homeTitle: '<i class="i-mdi-folder-multiple-outline" style="color: #2196f3; margin-right: 6px;"></i>文章分类',
    moreLabel: "更多 ...", // 查看更多分类标签
    emptyLabel: "暂无文章分类", // 分类为空时的标签
    limit: 8, // 一页显示的数量
    autoPage: false, // 是否自动翻页
    pageSpeed: 4000, // 翻页间隔时间，单位：毫秒。autoPage 为 true 时生效
  },
  // 标签卡片配置
  tag: {
    enabled: true, // 是否启用标签卡片
    path: "/tags", // 标签页访问地址
    pageTitle: '<i class="i-mdi-tag-multiple" style="color: #4caf50; margin-right: 6px;"></i>全部标签',
    homeTitle: '<i class="i-mdi-tag-multiple" style="color: #4caf50; margin-right: 6px;"></i>热门标签',
    moreLabel: "更多 ...", //  查看更多分类标签
    emptyLabel: "暂无标签", // 标签为空时的标签
    limit: 20, // 一页显示的数量
    autoPage: false, // 是否自动翻页
    pageSpeed: 4000, // 翻页间隔时间，单位：毫秒。autoPage 为 true 时生效
  },

  // ==========================================
  // ✅ Vite 插件配置
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