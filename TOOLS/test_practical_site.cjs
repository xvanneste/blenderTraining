/* Run after building SITE. Point PLAYWRIGHT_MODULE to an existing Playwright
 * installation if it is not in Node's module search path. */
const assert = require("node:assert/strict");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

async function main() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.BCMA_BROWSER,
    args: ["--allow-file-access-from-files"]
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    await page.addInitScript(() => {
      if (!localStorage.getItem("bcma.v1")) {
        localStorage.setItem("bcma.v1", JSON.stringify({
          done: { "CH01.02": true }, fav: { "CH01.02": true }, quiz: { "CH01.02": "9/10" }
        }));
      }
    });
    const url = pathToFileURL(path.join(__dirname, "..", "SITE", "index.html")).href;
    await page.goto(url);
    await page.getByRole("link", { name: "Ouvrir le parcours" }).click();
    assert.equal(await page.locator("main input[data-project]").count(), 3);
    const firstProject = page.getByRole("checkbox", { name: /Rendre une première image/ });
    await firstProject.check();
    assert.equal(await page.locator("#beginnerProgress").textContent(), "1 projet terminé sur 3");
    await page.reload();
    assert.equal(await firstProject.isChecked(), true);
    await page.getByRole("link", { name: "Ouvrir le brief court de la nature morte" }).click();
    const shortBrief = page.getByRole("heading", { name: "Version courte" });
    await shortBrief.waitFor();
    assert.equal(await shortBrief.evaluate(heading => heading === document.activeElement), true);
    await page.goto(url + "#bibliotheque");
    assert.equal(await page.locator(".library-phase li").count(), 199);
    await page.getByRole("searchbox", { name: "Sujet ou commande" }).fill("mecanique");
    await page.getByRole("searchbox", { name: "Sujet ou commande" }).press("Enter");
    await page.locator('#searchHits a[href*="CH06.07"]').first().waitFor();
    await page.reload();
    await page.getByRole("heading", { name: "Résultats de recherche" }).waitFor();
    await page.getByRole("searchbox", { name: "Sujet ou commande" }).fill("zzz-introuvable-9988");
    await page.getByRole("searchbox", { name: "Sujet ou commande" }).press("Enter");
    await page.getByText(/Aucun résultat/).waitFor();
    await page.goto(url + "#doc/START_HERE.md");
    await page.getByRole("link", { name: "Première image", exact: true }).click();
    const firstImage = page.getByRole("heading", { name: "Premier jalon — Rendre et conserver une image" });
    await firstImage.waitFor();
    assert.match(page.url(), /#ch\/CH00\.01\/TUTORIAL\.md\/premier-jalon--rendre-et-conserver-une-image$/);
    assert.equal(await firstImage.evaluate(heading => heading === document.activeElement), true);
    await page.goto(url + "#doc/DOCUMENTATION/PARCOURS_PREMIER_PLAN.md");
    await page.getByRole("link", { name: "suivi", exact: true }).click();
    assert.match(page.url(), /#doc\/PROGRESS\.md\/jalons-du-premier-plan$/);
    const checkpoint = page.locator("#jalons-du-premier-plan");
    await checkpoint.waitFor();
    assert.equal(await checkpoint.evaluate(heading => heading === document.activeElement), true);
    await page.goto(url + "#doc/DOCUMENTATION/GLOSSAIRE_BLENDER.md");
    await page.getByRole("link", { name: "CH01.08", exact: true }).click();
    await page.getByRole("heading", { name: /CH01\.08/ }).first().waitFor();
    await page.getByRole("tab", { name: "Tutoriels" }).click();
    await page.getByRole("heading", { name: "Contrôle de transfert" }).waitFor();
    await page.goto(url + "#ch/CH01.14/README.md");
    await page.getByRole("link", { name: "Projet de phase P1", exact: true }).click();
    await page.getByRole("heading", { name: "Corrigé à inspecter" }).waitFor();
    const stillLife = page.getByRole("img", { name: "Nature morte de référence rendue avec Cycles" });
    await page.waitForFunction(img => img.complete, await stillLife.elementHandle());
    assert.equal(await stillLife.evaluate(img => img.naturalWidth), 1920);
    await page.goto(url + "#ch/CH02.02");
    await page.getByRole("link", { name: "1. Caisse en bois" }).waitFor();
    await page.goto(url);
    await page.getByRole("link", { name: "Commencer la modélisation pratique" }).click();
    await page.locator(".atelier-index li").first().waitFor();
    assert.equal(await page.locator(".atelier-index li").count(), 19);
    await page.getByRole("link", { name: "1. Caisse en bois" }).click();
    await page.getByRole("link", { name: "Commencer →" }).click();
    await page.getByRole("checkbox").check();
    assert.equal(await page.locator("#atelierCheck").isChecked(), true);
    assert.equal(await page.locator("#atelierCount").textContent(), "1 / 5");
    await page.getByRole("link", { name: "Étape suivante →" }).click();
    await page.getByRole("heading", { name: "2. Créer la cavité" }).waitFor();
    await page.reload();
    await page.getByRole("heading", { name: "2. Créer la cavité" }).waitFor();
    await page.getByRole("link", { name: "← Précédent" }).click();
    await page.getByRole("heading", { name: "1. Bloquer l’encombrement" }).waitFor();
    assert.equal(await page.locator("#atelierCheck").isChecked(), true);
    await page.goto(url + "#atelier/caisse/quiz");
    await page.getByText("Créer le rebord", { exact: true }).click();
    await page.getByRole("button", { name: "Corriger" }).click();
    await page.getByText("Score : 1 / 1 — réussi.").waitFor();
    await page.goto(url + "#atelier/hum-corps/bassin");
    await page.getByRole("link", { name: "leçon 5" }).click();
    await page.getByRole("heading", { name: "Leçon 5 — Mirror et couture centrale" }).waitFor();
    await page.goto(url + "#atelier/projet-humain");
    await page.waitForFunction(() => {
      const video = document.querySelector("video");
      if (!video) return false;
      video.preload = "metadata";
      return video.readyState >= 1;
    }, null, { timeout: 12000 });
    assert.equal(await page.locator("video").evaluate(video => video.duration), 4);
    await page.goto(url + "#home");
    assert.match(await page.getByRole("link", { name: "Reprendre l’atelier Blender" }).getAttribute("href"),
      /#atelier\/projet-humain$/);
    const saved = await page.evaluate(() => JSON.parse(localStorage.getItem("bcma.v1")));
    assert.equal(saved.done["CH01.02"], true);
    assert.equal(saved.fav["CH01.02"], true);
    assert.equal(saved.quiz["CH01.02"], "9/10");
    assert.equal(saved.quiz["atelier/caisse"], "1/1");
    await page.setViewportSize({ width: 375, height: 760 });
    await page.goto(url + "#atelier/hum-import");
    await page.getByRole("heading", { name: "Leçon 3 — Importer et aligner les photos dans Blender" }).waitFor();
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    await page.goto(url + "#atelier/hum-import/face");
    const reference = page.locator('img[src$="04-images-ortho.png"]');
    await reference.waitFor();
    await page.waitForFunction(img => img.complete && img.naturalWidth > 0, await reference.elementHandle());
    await page.goto(url + "#atelier/projet-humain/export");
    const proof = page.locator('img[src$="08-reimport-export.png"]');
    await proof.waitFor();
    await page.waitForFunction(img => img.complete && img.naturalWidth > 0, await proof.elementHandle());
    assert.deepEqual(errors, []);
    console.log("Parcours, cases persistantes, reprise, quiz, lien interne, vidéo, mobile et anciennes données : OK.");
  } finally {
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
