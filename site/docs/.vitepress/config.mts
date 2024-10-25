import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Dooit",
  description: "Documentation for Dooit",
  base: '/dooit/',
  lastUpdated: true,
  themeConfig: {
    repo: 'dooit-org/dooit-extras',
    docsDir: 'site/docs',
    editLink: {
      pattern: 'https://github.com/dooit-org/dooit/edit/main/site/docs/:path',
      text: 'Edit this page on GitHub'
    },
    nav: [
      { text: "Home", link: "/" },
      { text: "Get Started", link: "/introduction" },
    ],
    socialLinks: [
      { icon: "github", link: "https://github.com/dooit-org/dooit" },
      { icon: "discord", link: "https://discord.com/invite/WA2ER9MBWa" },
      { icon: "twitter", link: "https://twitter.com/kraanzu" },
    ],
    search: {
      provider: "local"
    },
    sidebar: [
    ],
  }
})
