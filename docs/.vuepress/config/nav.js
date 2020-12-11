module.exports = [
  { text: '首页', link: '/' },
  {
    text: 'Python',
    link: '/Python/', //目录页链接，此处link是vdoing主题新增的配置项，有二级导航时，可以点击一级导航跳到目录页
    items: [
      // 说明：以下所有link的值只是在相应md文件定义的永久链接（不是什么特殊生成的编码）。另外，注意结尾是有斜杠的
      {
        text: '基础',
        items: [
          { text: 'JavaScript', link: '/wiki/8143cc480faf9a11/' },
          { text: 'Vue', link: '/wiki/802a1ca6f7b71c59/' },
        ],
      },
      {
        text: '进阶',
        items: [
          { text: 'Python 工匠系列', link: '/pythonisa/' },
          { text: '高阶知识点', link: '/advance/' },
        ],
      },
      {
        text: '指南',
        items: [
          { text: 'Socket 编程', link: '/socket/' },
          { text: '异步编程', link: '/async/' },
        ],
      },
    ],
  },
  {
    text: '规范',
    items: [
      { text: 'PEP', link: '/peps/' },
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
