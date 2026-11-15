/* Blender Cinema Master Academy — application de consultation hors ligne.
   Données : window.BCMA (data.js, généré par TOOLS/build_site.py).
   Mémoire locale (ce navigateur uniquement) : progression, scores de quiz, favoris, dernier onglet. */
(function () {
  "use strict";
  var D = window.BCMA;
  var main = document.getElementById("main");
  var nav = document.getElementById("nav");
  var KEY = "bcma.v1";

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* stockage indisponible */ } }
  var S = load(); S.done = S.done || {}; S.fav = S.fav || {}; S.quiz = S.quiz || {};

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function stIcon(s) { return s.indexOf("✅") >= 0 ? "✅" : s.indexOf("🟦") >= 0 ? "🟦" : s.indexOf("🟨") >= 0 ? "🟨" : "⬜"; }
  function available(code) { return !!D.chapters[code]; }
  function allChapters() { var r = []; D.phases.forEach(function (p) { p.chapters.forEach(function (c) { r.push(c); }); }); return r; }

  function badge() {
    var avail = allChapters().filter(function (c) { return c.status.indexOf("✅") >= 0; }).length;
    var done = Object.keys(S.done).filter(function (k) { return S.done[k]; }).length;
    document.getElementById("progressBadge").textContent = "Acquis : " + done + " / " + avail + " disponibles";
  }

  function buildNav() {
    var h = '<h3>Général</h3>';
    h += '<a class="item" href="#home"><span class="st">🏠</span>Tableau de bord</a>';
    h += '<a class="item" href="#favoris"><span class="st">★</span>Favoris</a>';
    h += '<a class="item" href="#fiches"><span class="st">📄</span>Fiches de révision</a>';
    D.general.forEach(function (g) { h += '<a class="item" href="#doc/' + encodeURIComponent(g.id) + '"><span class="st">📘</span>' + esc(g.label) + '</a>'; });
    h += '<h3>Programme</h3>';
    D.phases.forEach(function (p) {
      var ok = p.chapters.filter(function (c) { return c.status.indexOf("✅") >= 0; }).length;
      h += '<details' + (ok ? " open" : "") + '><summary>Phase ' + p.num + ' — ' + esc(p.title) +
        '<span class="count">' + ok + "/" + p.chapters.length + '</span></summary>';
      p.chapters.forEach(function (c) {
        var mine = S.done[c.code] ? "🟩" : stIcon(c.status);
        h += '<a class="item' + (available(c.code) ? "" : " off") + '" data-code="' + c.code + '" href="#ch/' + c.code + '"><span class="st">' +
          mine + '</span><span>' + c.code + " " + esc(c.title) + '</span></a>';
      });
      h += "</details>";
    });
    nav.innerHTML = h;
  }

  function home() {
    var all = allChapters();
    var avail = all.filter(function (c) { return c.status.indexOf("✅") >= 0; });
    var done = avail.filter(function (c) { return S.done[c.code]; });
    var next = avail.filter(function (c) { return !S.done[c.code]; })[0];
    var pct = avail.length ? Math.round(100 * done.length / avail.length) : 0;
    var h = '<h1>Tableau de bord</h1>';
    h += '<div class="cards">';
    h += '<div class="card"><div class="big">' + D.stats.done + ' / ' + D.stats.total + '</div>chapitres produits et vérifiés dans l\'académie</div>';
    h += '<div class="card"><div class="big">' + done.length + '</div>chapitres marqués « acquis » par vous<div class="bar"><span style="width:' + pct + '%"></span></div></div>';
    h += '<div class="card"><div class="big">' + Object.keys(S.quiz).length + '</div>quiz passés</div>';
    h += '</div>';
    if (next) { h += '<p>Prochain chapitre conseillé : <a href="#ch/' + next.code + '">' + next.code + ' ' + esc(next.title) + '</a></p>'; }
    h += '<h2>Par phase</h2><div class="cards">';
    D.phases.forEach(function (p) {
      var ok = p.chapters.filter(function (c) { return c.status.indexOf("✅") >= 0; }).length;
      var mine = p.chapters.filter(function (c) { return S.done[c.code]; }).length;
      h += '<div class="card"><strong>Phase ' + p.num + '</strong><br>' + esc(p.title) + '<br><small>' + ok + '/' + p.chapters.length +
        ' produits · ' + mine + ' acquis</small><div class="bar"><span style="width:' + (p.chapters.length ? 100 * ok / p.chapters.length : 0) + '%"></span></div></div>';
    });
    h += '</div><p class="crumbs">La progression, les favoris et les scores sont enregistrés dans ce navigateur uniquement.</p>';
    main.innerHTML = h;
  }

  function findChapter(code) { var r = null; D.phases.forEach(function (p) { p.chapters.forEach(function (c) { if (c.code === code) r = { ch: c, phase: p }; }); }); return r; }

  function chapter(code, tab) {
    var f = findChapter(code); if (!f) { home(); return; }
    var c = f.ch, data = D.chapters[code];
    var h = '<div class="crumbs">Phase ' + f.phase.num + ' — ' + esc(f.phase.title) + '</div>';
    h += '<h1>' + code + ' — ' + esc(c.title) + '</h1><div class="crumbs">' + esc(c.status) + '</div>';
    if (!data) { main.innerHTML = h + '<p>Ce chapitre n\'est pas encore produit. Voir le <a href="#doc/CURRICULUM.md">programme</a>.</p>'; return; }
    h += '<div class="actions"><button class="btn' + (S.done[code] ? " on" : "") + '" id="doneBtn">' + (S.done[code] ? "✔ Acquis" : "Marquer comme acquis") +
      '</button><button class="btn fav' + (S.fav[code] ? " on" : "") + '" id="favBtn">' + (S.fav[code] ? "★ Favori" : "☆ Ajouter aux favoris") + '</button>';
    if (c.dir) h += '<a class="btn" href="../' + c.dir + '/">📁 Ouvrir le dossier</a>';
    h += '</div><div class="tabs" role="tablist">';
    var tabs = Object.keys(data.docs);
    if (data.quiz) tabs.push("QUIZ");
    if (data.images.length) tabs.push("IMAGES");
    tab = tab && tabs.indexOf(tab) >= 0 ? tab : (S.tab && tabs.indexOf(S.tab) >= 0 ? S.tab : tabs[0]);
    tabs.forEach(function (t) {
      var label = t === "QUIZ" ? "Quiz" + (S.quiz[code] ? " (" + S.quiz[code] + ")" : "") : t === "IMAGES" ? "Images" : data.docs[t].label;
      h += '<button role="tab" aria-selected="' + (t === tab) + '" data-tab="' + t + '">' + esc(label) + '</button>';
    });
    h += '</div><div class="doc" id="tabBody"></div>';
    main.innerHTML = h;
    document.getElementById("doneBtn").onclick = function () { S.done[code] = !S.done[code]; save(S); buildNav(); badge(); chapter(code, tab); };
    document.getElementById("favBtn").onclick = function () { S.fav[code] = !S.fav[code]; save(S); chapter(code, tab); };
    Array.prototype.forEach.call(main.querySelectorAll(".tabs button"), function (b) {
      b.onclick = function () { S.tab = b.getAttribute("data-tab"); save(S); location.hash = "#ch/" + code + "/" + S.tab; };
    });
    var body = document.getElementById("tabBody");
    if (tab === "QUIZ") quiz(body, code, data.quiz);
    else if (tab === "IMAGES") body.innerHTML = '<div class="gallery">' + data.images.map(function (src) { return '<a href="' + esc(src) + '" target="_blank"><img loading="lazy" src="' + esc(src) + '" alt="' + esc(src.split("/").pop()) + '"></a>'; }).join("") + "</div>";
    else body.innerHTML = data.docs[tab].html;
    Array.prototype.forEach.call(nav.querySelectorAll("a.item"), function (a) { a.classList.toggle("active", a.getAttribute("data-code") === code); });
  }

  function quiz(body, code, Q) {
    var h = '<div class="quiz"><p>Seuil de réussite : ' + Q.pass_score + ' / ' + Q.questions.length +
      '. Les QCM sont corrigés automatiquement ; pour les questions ouvertes, répondez puis comparez avec la réponse et cochez si elle est juste.</p>';
    Q.questions.forEach(function (q, i) {
      h += '<div class="q" data-i="' + i + '"><strong>' + q.id + '.</strong> ' + esc(q.q);
      if (q.type === "mcq") {
        q.choices.forEach(function (ch, j) { h += '<label><input type="radio" name="q' + i + '" value="' + j + '"> ' + esc(ch) + '</label>'; });
      } else {
        h += '<textarea rows="2" style="width:100%;margin-top:6px" aria-label="Votre réponse"></textarea>' +
          '<div class="expl" hidden><strong>Réponse attendue :</strong> ' + esc(q.answer_text) +
          '<label><input type="checkbox" class="self"> Ma réponse est juste</label></div>';
      }
      h += '</div>';
    });
    h += '<button class="btn" id="check">Corriger</button><div id="res"></div></div>';
    body.innerHTML = h;
    document.getElementById("check").onclick = function () {
      var score = 0, pending = false;
      Q.questions.forEach(function (q, i) {
        var box = body.querySelector('.q[data-i="' + i + '"]');
        if (q.type === "mcq") {
          var sel = box.querySelector("input:checked");
          Array.prototype.forEach.call(box.querySelectorAll("label"), function (l, j) {
            l.classList.remove("good", "bad");
            if (j === q.answer) l.classList.add("good");
            else if (sel && +sel.value === j) l.classList.add("bad");
          });
          if (sel && +sel.value === q.answer) score++;
          if (!box.querySelector(".expl")) box.insertAdjacentHTML("beforeend", '<div class="expl">' + esc(q.explain || "") + "</div>");
        } else {
          var ex = box.querySelector(".expl");
          if (ex.hidden) { ex.hidden = false; pending = true; }
          if (box.querySelector(".self").checked) score++;
        }
      });
      var ok = score >= Q.pass_score;
      document.getElementById("res").innerHTML = '<div class="result ' + (ok ? "ok" : "ko") + '">Score : ' + score + " / " + Q.questions.length +
        (pending ? " — cochez vos réponses ouvertes justes puis cliquez à nouveau sur Corriger." : ok ? " — réussi." : " — à retravailler.") + "</div>";
      if (!pending) { S.quiz[code] = score + "/" + Q.questions.length; save(S); }
    };
  }

  function docPage(id) {
    var g = D.general.filter(function (x) { return x.id === id; })[0];
    main.innerHTML = g ? '<div class="doc">' + g.html + "</div>" : "<p>Document introuvable.</p>";
  }

  function sheets() {
    var h = "<h1>Fiches de révision</h1>";
    D.sheets.forEach(function (s) { h += '<details class="card" style="margin:8px 0"><summary><strong>' + esc(s.label) + '</strong></summary><div class="doc">' + s.html + "</div></details>"; });
    main.innerHTML = h;
  }

  function favorites() {
    var codes = Object.keys(S.fav).filter(function (k) { return S.fav[k]; });
    var h = "<h1>Favoris</h1>";
    h += codes.length ? "<ul>" + codes.map(function (c) { var f = findChapter(c); return '<li><a href="#ch/' + c + '">' + c + " " + esc(f ? f.ch.title : "") + "</a></li>"; }).join("") + "</ul>"
      : "<p>Aucun favori. Utilisez « ☆ Ajouter aux favoris » sur une page de chapitre.</p>";
    main.innerHTML = h;
  }

  function search(q) {
    q = q.trim().toLowerCase();
    if (q.length < 2) { route(); return; }
    var words = q.split(/\s+/), hits = [];
    function rx(w) { return new RegExp("(^|[^\\p{L}\\p{N}])" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?=$|[^\\p{L}\\p{N}])", "giu"); }
    var wordRx = words.map(rx), phraseRx = rx(q.replace(/\s+/g, " "));
    function count(re, t) { var m = t.match(re); return m ? m.length : 0; }
    // mots entiers obligatoires ; l'expression exacte compte beaucoup plus
    function score(text) { var t = text.replace(/\s+/g, " "), s = 0; for (var i = 0; i < wordRx.length; i++) { var n = count(wordRx[i], t); if (!n) return 0; s += n; } return s + 50 * count(phraseRx, t); }
    function snippet(text) { var t = text.replace(/\s+/g, " "), k = t.toLowerCase().indexOf(words[0]); var s = t.substr(Math.max(0, k - 60), 180); return esc(s).replace(new RegExp(words.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|"), "gi"), function (m) { return "<mark>" + m + "</mark>"; }); }
    Object.keys(D.chapters).forEach(function (code) {
      var f = findChapter(code); var docs = D.chapters[code].docs;
      Object.keys(docs).forEach(function (t) { var s = score(docs[t].text); if (s) hits.push({ s: s, href: "#ch/" + code + "/" + t, title: code + " " + (f ? f.ch.title : "") + " — " + docs[t].label, snip: snippet(docs[t].text) }); });
    });
    D.general.concat(D.sheets).forEach(function (g) { var s = score(g.text); if (s) hits.push({ s: s, href: D.general.indexOf(g) >= 0 ? "#doc/" + encodeURIComponent(g.id) : "#fiches", title: g.label, snip: snippet(g.text) }); });
    hits.sort(function (a, b) { return b.s - a.s; });
    main.innerHTML = "<h1>Recherche : « " + esc(q) + " »</h1><p class=\"crumbs\">" + hits.length + " résultat(s)</p>" +
      hits.slice(0, 60).map(function (h) { return '<div class="hit"><a href="' + h.href + '">' + esc(h.title) + "</a><br><small>… " + h.snip + " …</small></div>"; }).join("");
  }

  function route() {
    var h = decodeURIComponent(location.hash.slice(1)).split("/");
    nav.classList.remove("open");
    if (h[0] === "ch") chapter(h[1], h[2]);
    else if (h[0] === "doc") docPage(h.slice(1).join("/"));
    else if (h[0] === "fiches") sheets();
    else if (h[0] === "favoris") favorites();
    else home();
    main.focus(); window.scrollTo(0, 0);
  }

  var timer;
  document.getElementById("q").addEventListener("input", function (e) { clearTimeout(timer); var v = e.target.value; timer = setTimeout(function () { search(v); }, 200); });
  document.getElementById("menuBtn").onclick = function () { nav.classList.toggle("open"); };
  window.addEventListener("hashchange", route);
  buildNav(); badge(); route();
})();
