/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: process.env.SITE_URL || "https://eldhopaulose.github.io",
  generateRobotsTxt: true,
  outDir: "./public",
};
