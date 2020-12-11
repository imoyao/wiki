module.exports = [
  { text: '首页', link: '/' },
  {
    text: '前端',
    link: '/web/', //目录页链接，此处link是vdoing主题新增的配置项，有二级导航时，可以点击一级导航跳到目录页
    items: [
      // 说明：以下所有link的值只是在相应md文件定义的永久链接（不是什么特殊生成的编码）。另外，注意结尾是有斜杠的
      {
        text: '前端文章',
        items: [
          { text: 'JavaScript', link: '/wiki/8143cc480faf9a11/' },
          { text: 'Vue', link: '/wiki/802a1ca6f7b71c59/' },
        ],
      },
      {
        text: '学习笔记',
        items: [
          { text: '《JavaScript教程》笔记', link: '/note/javascript/' },
          { text: '《JavaScript高级程序设计》笔记', link: '/note/js/' },
          { text: '《ES6 教程》笔记', link: '/note/es6/' },
          { text: '《Vue》笔记', link: '/note/vue/' },
          {
            text: '《TypeScript 从零实现 axios》',
            link: '/note/typescript-axios/',
          },
          {
            text: '《Git》学习笔记',
            link: '/note/git/',
          },
          {
            text: '《TypeScript》笔记',
            link: '/wiki/51afd6/',
          },
        ],
      },
    ],
  },
  {
    text: 'Python',
    link: '/python/',
    items: [
      { text: 'HTML', link: '/wiki/8309a5b876fc95e3/' },
      { text: 'CSS', link: '/wiki/0a83b083bdf257cb/' },
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
