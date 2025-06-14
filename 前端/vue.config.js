const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './',
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html'
    },
    // log: {
    //   entry: 'src/log.js',
    //   template: 'public/log.html',
    //   filename: 'log.html'
    // },
    // grzx: {
    //   entry: 'src/grzx.js',
    //   template: 'public/grzx.html',
    //   filename: 'grzx.html'
    // }
    }
})
