/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: process.env.SITE_URL || "https://eldhopaulose.info",
  generateRobotsTxt: true,
  outDir: "./out",
};
