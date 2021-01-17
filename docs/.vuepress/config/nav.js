module.exports = [
  { text: '首页', link: '/' },
  {
    text: 'Python',
    link: '/python/', //目录页链接，此处link是vdoing主题新增的配置项，有二级导航时，可以点击一级导航跳到目录页
    items: [
      // 说明：以下所有link的值只是在相应md文件定义的永久链接（不是什么特殊生成的编码）。另外，注意结尾是有斜杠的
      {
        text: '基础',
        items: [
          { text: '全栈之路', link: '/python/fullstack/index/' },
          { text: '😎Awesome资源', link: '/python/awesome/index/' },
        ],
      },
      {
        text: '进阶',
        items: [
          { text: 'Python 工匠系列', link: '/craftsman/index/' },
          { text: '高阶知识点', link: '/python/GIL/' },
        ],
      },
      {
        text: '指南教程',
        items: [
          { text: 'Socket 编程', link: '/socket/index/' },
          { text: '异步编程', link: '/python/async/index/' },
        ],
      },
    ],
  },
  {
    text: '其他',
    items: [
      { text: 'Git 参考手册', link: '/git/reference/' },
    ],
  },
  {
    text: '理财',
    items: [
      { text: '基金知识', link: '/funds/04a189/' },
      { text: '基金经理', link: '/mgr/635a97/' },
    ],
  },
  {
    text: '索引',
    link: '/archives/',
    items: [
      { text: '分类', link: '/categories/' },
      { text: '标签', link: '/tags/' },
      { text: '归档', link: '/archives/' },
    ],
  },
]
