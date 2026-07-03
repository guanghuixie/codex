import { chromium } from "/Users/xieguanghui/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";
import fs from "node:fs";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
await page.goto("file:///Library/study/0703codex/index.html");
await page.fill("#todo-input", "部署监控看板");
await page.click('button[type="submit"]');
await page.fill("#todo-input", "整理 Go 服务日志");
await page.click('button[type="submit"]');

const result = {
  title: await page.textContent("#app-title"),
  itemCount: await page.locator(".todo-item").count(),
  panelBox: await page.locator(".todo-panel").boundingBox(),
  inputBox: await page.locator("#todo-input").boundingBox(),
  activeFilterColor: await page.locator(".filter-button.active").evaluate((node) => getComputedStyle(node).backgroundColor),
};

await page.screenshot({ path: "todo-tech-preview.png", fullPage: true });
await browser.close();
fs.writeFileSync("visual-check-result.json", `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
