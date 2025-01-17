module.exports = {
  setupFilesAfterEnv: ["<rootDir>/jest-setup.js"],
  preset: "@vue/cli-plugin-unit-jest",
  transformIgnorePatterns: ["node_modules/(?!axios)"],
};
