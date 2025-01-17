const { defineConfig } = require("@vue/cli-service");
const config = defineConfig({
  transpileDependencies: true,
});

// vue.config.js
module.exports = {
  devServer: {
    proxy: "http://localhost:5000",
  },
  configureWebpack: {
    devtool: "source-map",
  },
  chainWebpack: (config) => {
    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => ({
        ...options,
        compilerOptions: {
          // treat any tag that starts with cs- as custom elements
          isCustomElement: (tag) => tag.startsWith("admin-"),
        },
      }));
  },
};
