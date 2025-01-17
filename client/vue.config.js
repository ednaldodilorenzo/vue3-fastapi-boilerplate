const { defineConfig } = require("@vue/cli-service");
const config = defineConfig({
  transpileDependencies: true,
});

// vue.config.js
module.exports = {
  pluginOptions: {
    s3Deploy: {
      region: "sa-east-1",
      bucket: "gestor-paroquial-spa",
      staticHosting: true,
      acl: "public-read",
      gzip: "true",
      registry: undefined,
      awsProfile: "default",
      overrideEndpoint: false,
      createBucket: true,
      staticIndexPage: "index.html",
      staticErrorPage: "error.html",
      assetPath: "dist",
      assetMatch: "**",
      deployPath: "/",
      pwa: false,
      enableCloudfront: false,
      pluginVersion: "4.0.0-rc3",
      uploadConcurrency: 5,
    },
  },
  devServer: {
    proxy: "http://localhost:8000",
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
