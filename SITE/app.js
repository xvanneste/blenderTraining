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
  S.practice = S.practice || {};
  S.beginner = S.beginner || {};
  if (!/^#atelier\/[a-z0-9-]+(?:\/[a-z0-9-]+)?$/.test(S.practiceLast || "")) S.practiceLast = "";

  function practiceURL(unit, step) {
    return "#atelier/" + unit.id + (step ? "/" + step : "");
  }
  function practiceUnits() {
    return D.modeling.reduce(function (units, group) { return units.concat(group.units); }, []);
  }
  function unitChecks(unit) {
    return S.practice[unit.id] || {};
  }
  function practiceCount(unit) {
    var checks = unitChecks(unit);
    return unit.steps.filter(function (step) { return !!checks[step.id]; }).length;
  }

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function allChapters() { var r = []; D.phases.forEach(function (p) { p.chapters.forEach(function (c) { r.push(c); }); }); return r; }

  function badge() {
    document.getElementById("progressBadge").textContent = beginnerLabel();
  }

  function buildNav() {
    var h = '<h3>Deux lectures</h3>';
    h += '<a class="item" href="#home">Accueil</a>';
    h += '<a class="item" href="#parcours">Parcours débutant</a>';
    h += '<a class="item" href="#bibliotheque">Bibliothèque</a>';
    h += '<h3>Accès directs</h3>';
    h += '<a class="item" href="#atelier"><span class="st">◈</span>Modéliser dans Blender</a>';
    h += '<a class="item" href="#favoris"><span class="st">★</span>Favoris</a>';
    h += '<a class="item" href="#fiches"><span class="st">📄</span>Fiches de révision</a>';
    nav.innerHTML = h;
  }

  function library() {
    var h = '<h1>Bibliothèque Blender</h1><p>' + allChapters().length + ' chapitres à consulter par sujet.</p>' + searchForm('');
    h += '<h2>Chapitres par phase</h2>';
    D.phases.forEach(function (p) {
      h += '<details class="library-phase"><summary>Phase ' + p.num + ' — ' + esc(p.title) + '</summary><ul>';
      p.chapters.forEach(function (c) {
        h += '<li><a href="#ch/' + c.code + '">' + c.code + " " + esc(c.title) + '</a>' + (S.done[c.code] ? ' <small>· Acquis</small>' : '') + '</li>';
      });
      h += "</ul></details>";
    });
    h += '<h2>Guides et références</h2><ul>';
    D.general.forEach(function (g) { h += '<li><a href="#doc/' + encodeURIComponent(g.id) + '">' + esc(g.label) + '</a></li>'; });
    main.innerHTML = h + '</ul>';
    bindSearch();
  }

  var beginnerProjects = [
    {
      id: "image", title: "Rendre une première image",
      links: [["Installer Blender", "#ch/CH00.01"], ["Rendre et enregistrer la mire", "#ch/CH00.01/TUTORIAL.md/premier-jalon--rendre-et-conserver-une-image"]],
      proof: "Gardez une copie .blend et un PNG lisible. Rouvrez le PNG, puis refaites un rendu et enregistrez une seconde image sans le guide."
    },
    {
      id: "caisse", title: "Créer un objet de bout en bout",
      links: [["Modéliser la caisse", "#atelier/caisse"], ["Ajouter un matériau", "#ch/CH01.11/TUTORIAL.md"], ["Cadrer la caisse", "#ch/CH01.12/TUTORIAL.md"], ["Installer une lumière principale", "#ch/CH01.13/TUTORIAL.md"], ["Rendre l’image", "#ch/CH01.14/TUTORIAL.md"]],
      proof: "Livrez caisse.blend et un rendu où le vide et le rebord sont lisibles. Dans une copie, changez la largeur de la caisse et adaptez un renfort sans le tutoriel."
    },
    {
      id: "scene", title: "Réaliser une petite nature morte",
      links: [["Ouvrir le brief court de la nature morte", "#doc/01_FUNDAMENTALS/PROJECT_P1/README.md/version-courte"]],
      proof: "Sur une table, placez votre caisse et deux objets simples. Produisez une image carrée avec un sujet principal lisible. Reprenez le cadrage seul dans une copie. La grille du projet P1 sert à évaluer la composition, la lumière et la possibilité de rouvrir la scène. Vous pourrez ensuite essayer le projet P1 complet."
    }
  ];

  function beginnerLabel() {
    var count = beginnerProjects.filter(function (project) { return S.beginner[project.id]; }).length;
    return count + (count > 1 ? " projets terminés sur " : " projet terminé sur ") + beginnerProjects.length;
  }

  function home() {
    var h = '<h1>Apprendre Blender</h1><div class="cards reading-cards">';
    h += '<section class="card"><h2>Parcours débutant</h2><p>Trois projets pour rendre une image, construire un objet et réaliser une petite scène.</p>';
    h += '<p><strong>' + beginnerLabel() + '</strong></p><a class="btn" href="#parcours">Ouvrir le parcours</a></section>';
    h += '<section class="card"><h2>Bibliothèque Blender</h2><p>Retrouvez une commande, un tutoriel ou une spécialité parmi les ' + allChapters().length + ' chapitres.</p>';
    h += '<a class="btn" href="#bibliotheque">Ouvrir la bibliothèque</a></section></div>';
    h += '<p><a href="' + (S.practiceLast ? esc(S.practiceLast) : "#atelier") + '">' +
      (S.practiceLast ? "Reprendre l’atelier Blender" : "Commencer la modélisation pratique") + '</a></p>';
    main.innerHTML = h;
  }

  function beginner() {
    var h = '<h1>Parcours débutant</h1><p id="beginnerProgress" role="status">' + beginnerLabel() + '</p><ol class="projects">';
    beginnerProjects.forEach(function (project) {
      h += '<li class="card"><h2>' + esc(project.title) + '</h2><ul>';
      project.links.forEach(function (link) {
        h += '<li><a href="' + link[1] + '">' + esc(link[0]) + '</a></li>';
      });
      h += '</ul><p>' + esc(project.proof) + '</p><label class="atelier-check"><input type="checkbox" data-project="' + project.id +
        '"' + (S.beginner[project.id] ? ' checked' : '') + '> ' + esc(project.title) + ' · livrable vérifié</label></li>';
    });
    h += '</ol><h2>Choisir la suite</h2><ul><li><a href="#atelier">Modélisation et personnage</a></li>' +
      '<li><a href="#doc/DOCUMENTATION/PARCOURS_PREMIER_PLAN.md">Animation et premier plan</a></li>' +
      '<li><a href="#bibliotheque">Toutes les spécialités dans la bibliothèque</a></li></ul>';
    main.innerHTML = h;
    main.querySelectorAll('[data-project]').forEach(function (box) {
      box.addEventListener('change', function () {
        S.beginner[box.dataset.project] = box.checked;
        save(S);
        badge();
        document.getElementById('beginnerProgress').textContent = beginnerLabel();
      });
    });
  }

  function practice(unitId, stepId) {
    var units = practiceUnits();
    var index = units.findIndex(function (unit) { return unit.id === unitId; });
    if (index < 0) {
      var h = '<h1>Modéliser dans Blender</h1><p>Du premier maillage au personnage humain. Réalisez les étapes dans Blender et cochez-les ici après vérification.</p>';
      if (S.practiceLast) h += '<p><a class="btn" href="' + esc(S.practiceLast) + '">Reprendre mon atelier</a></p>';
      D.modeling.forEach(function (group) {
        h += '<h2>' + esc(group.title) + '</h2><ul class="atelier-index">';
        group.units.forEach(function (unit) {
          h += '<li><a href="' + practiceURL(unit) + '">' + esc(unit.title) + '</a><span>' +
            practiceCount(unit) + ' / ' + unit.steps.length + ' étapes</span></li>';
        });
        h += '</ul>';
      });
      main.innerHTML = h;
      return;
    }
    var unit = units[index], checks = unitChecks(unit);
    var stepIndex = unit.steps.findIndex(function (step) { return step.id === stepId; });
    var step = unit.steps[stepIndex];
    var isQuiz = stepId === "quiz" && unit.quiz && unit.quiz.length;
    S.practiceLast = practiceURL(unit, step ? step.id : isQuiz ? "quiz" : "");
    save(S);
    var h = '<div class="crumbs"><a href="#atelier">Sommaire de modélisation</a></div>';
    h += '<h1>' + esc(unit.title) + '</h1><progress id="atelierProgress" max="' + unit.steps.length +
      '" value="' + practiceCount(unit) + '" aria-label="Étapes réalisées"></progress> <span id="atelierCount">' +
      practiceCount(unit) + ' / ' + unit.steps.length + '</span>';
    h += '<details class="card atelier-toc"' + (step || isQuiz ? "" : " open") + '><summary>Objectif et sommaire de l’atelier</summary>';
    h += '<p><a href="' + practiceURL(unit) + '">Brief, supports et erreurs fréquentes</a></p>';
    h += '<ol>' + unit.steps.map(function (s) {
      return '<li><a' + (s === step ? ' aria-current="step"' : "") + ' href="' + practiceURL(unit,s.id) +
        '">' + esc(s.title) + '</a>' + (checks[s.id] ? ' <span aria-label="Réalisée">✓</span>' : '') + '</li>';
    }).join("") + '</ol>';
    if (unit.quiz && unit.quiz.length) {
      var score = S.quiz["atelier/" + unit.id];
      h += '<a href="' + practiceURL(unit,"quiz") + '">Quiz de vérification' +
        (score ? " (" + esc(score) + ")" : "") + '</a>';
    }
    h += '</details><div class="atelier-keys" aria-label="Raccourcis Blender">' +
      unit.keys.map(function (key) { return '<kbd>' + esc(key) + '</kbd>'; }).join(" ") + '</div>';
    if (isQuiz) h += '<div id="atelierQuiz"></div>';
    else if (step) {
      h += '<h2>' + (stepIndex + 1) + '. ' + esc(step.title) + '</h2><div class="doc">' + step.html + '</div>';
      h += '<label class="card atelier-check"><input id="atelierCheck" type="checkbox"' + (checks[step.id] ? ' checked' : '') +
        '> J’ai fait cette étape dans Blender et vérifié le résultat.</label>';
    } else {
      h += '<div class="doc">' + unit.intro + '</div>';
      if (unit.video) h += '<p><video controls preload="none" aria-label="Démonstration du résultat final" src="' + esc(unit.video) + '"></video></p>';
    }
    h += '<div class="actions atelier-actions">';
    if (stepIndex >= 0) h += '<a class="btn" href="' +
      practiceURL(unit, stepIndex > 0 ? unit.steps[stepIndex - 1].id : "") + '">← Précédent</a>';
    else if (isQuiz) h += '<a class="btn" href="' + practiceURL(unit,unit.steps[unit.steps.length-1].id) + '">← Dernière étape</a>';
    else if (index > 0) h += '<a class="btn" href="' + practiceURL(units[index - 1]) + '">← Atelier précédent</a>';
    if (!isQuiz && stepIndex + 1 < unit.steps.length) h += '<a class="btn on" href="' +
      practiceURL(unit,unit.steps[stepIndex + 1].id) + '">' + (step ? "Étape suivante →" : "Commencer →") + '</a>';
    else if (!isQuiz && unit.quiz && unit.quiz.length) h += '<a class="btn on" href="' + practiceURL(unit,"quiz") + '">Faire le quiz →</a>';
    else if (index + 1 < units.length) h += '<a class="btn on" href="' + practiceURL(units[index + 1]) + '">Atelier suivant →</a>';
    else h += '<a class="btn" href="#atelier">Retour au sommaire</a>';
    main.innerHTML = h + '</div>';
    if (isQuiz) quiz(document.getElementById("atelierQuiz"), "atelier/" + unit.id,
      { pass_score: Math.ceil(unit.quiz.length * 0.8), questions: unit.quiz });
    if (step) {
      document.getElementById("atelierCheck").onchange = function () {
        var tocOpen = main.querySelector(".atelier-toc").open;
        checks[step.id] = this.checked;
        S.practice[unit.id] = checks;
        save(S);
        practice(unit.id, step.id);
        main.querySelector(".atelier-toc").open = tocOpen;
        document.getElementById("atelierCheck").focus();
      };
    }
  }

  function findChapter(code) { var r = null; D.phases.forEach(function (p) { p.chapters.forEach(function (c) { if (c.code === code) r = { ch: c, phase: p }; }); }); return r; }

  function chapter(code, tab) {
    var f = findChapter(code); if (!f) { home(); return; }
    var c = f.ch, data = D.chapters[code];
    var h = '<div class="crumbs">Phase ' + f.phase.num + ' — ' + esc(f.phase.title) + '</div>';
    h += '<h1>' + code + ' — ' + esc(c.title) + '</h1><div class="crumbs">' + esc(c.evidence || c.status) + '</div>';
    if (!data) { main.innerHTML = h + '<p>Ce chapitre n\'est pas encore produit. Voir le <a href="#doc/CURRICULUM.md">programme</a>.</p>'; return; }
    h += '<div class="actions"><button class="btn' + (S.done[code] ? " on" : "") + '" id="doneBtn">' + (S.done[code] ? "✔ Acquis" : "Marquer comme acquis") +
      '</button><button class="btn fav' + (S.fav[code] ? " on" : "") + '" id="favBtn">' + (S.fav[code] ? "★ Favori" : "☆ Ajouter aux favoris") + '</button>';
    if (c.dir) h += '<a class="btn" href="../' + c.dir + '/">📁 Ouvrir le dossier</a>';
    h += '</div>';
    if (data.practice) {
      h += '<div class="actions"><span>À pratiquer dans Blender</span>';
      practiceUnits().filter(function (unit) { return data.practice.indexOf(unit.id) >= 0; }).forEach(function (unit) {
        h += '<a class="btn" href="' + practiceURL(unit) + '">' + esc(unit.title) + '</a>';
      });
      h += '</div>';
    }
    h += '<div class="tabs" role="tablist">';
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

  function sheets(selected) {
    var h = "<h1>Fiches de révision</h1>";
    D.sheets.forEach(function (s, index) { h += '<details class="card" id="fiche-' + index + '" tabindex="-1"' + (String(index) === selected ? ' open' : '') + ' style="margin:8px 0"><summary><strong>' + esc(s.label) + '</strong></summary><div class="doc">' + s.html + "</div></details>"; });
    main.innerHTML = h;
  }

  function favorites() {
    var codes = Object.keys(S.fav).filter(function (k) { return S.fav[k]; });
    var h = "<h1>Favoris</h1>";
    h += codes.length ? "<ul>" + codes.map(function (c) { var f = findChapter(c); return '<li><a href="#ch/' + c + '">' + c + " " + esc(f ? f.ch.title : "") + "</a></li>"; }).join("") + "</ul>"
      : "<p>Aucun favori. Utilisez « ☆ Ajouter aux favoris » sur une page de chapitre.</p>";
    main.innerHTML = h;
  }

  function searchForm(query) {
    return '<form id="librarySearch" class="search library-search" role="search" aria-label="Recherche dans les cours">' +
      '<input type="search" name="query" aria-label="Sujet ou commande" placeholder="Ex. retopologie, Rigify, passe Z" ' +
      'required minlength="2" maxlength="150" value="' + esc(query) + '"><button class="btn" type="submit">Chercher</button></form>';
  }

  function openSearch(query) {
    query = query.trim();
    if (query.length < 2) return;
    var hash = "#recherche/" + encodeURIComponent(query);
    if (location.hash === hash) route();
    else location.hash = hash;
  }

  function bindSearch() {
    var form = document.getElementById("librarySearch");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      openSearch(form.elements.query.value);
    });
  }

  function normalizeSearch(text) {
    return text.toLowerCase().normalize("NFD").replace(/\p{M}/gu, "").replace(/\s+/g, " ");
  }

  function search(query) {
    var normalized = normalizeSearch(query.trim());
    var words = normalized.match(/[\p{L}\p{N}]+/gu) || [];
    var hits = [];
    function add(href, title, body) {
      var text = normalizeSearch(body);
      var name = normalizeSearch(title);
      if (!words.length || !words.every(function (word) { return name.includes(word) || text.includes(word); })) return;
      var score = words.reduce(function (sum, word) { return sum + (name.includes(word) ? 8 : 1); }, 0);
      if (name.includes(normalized)) score += 24;
      if (text.includes(normalized)) score += 10;
      var index = text.indexOf(normalized);
      if (index < 0) index = text.indexOf(words[0]);
      var start = Math.max(0, index - 44);
      hits.push({ href: href, title: title, score: score, snippet: body.replace(/\s+/g, " ").slice(start, start + 170) });
    }
    allChapters().forEach(function (chapter) {
      var data = D.chapters[chapter.code];
      if (!data) return;
      Object.keys(data.docs).forEach(function (tab) {
        var doc = data.docs[tab];
        add("#ch/" + chapter.code + "/" + tab, chapter.code + " " + chapter.title + " — " + doc.label, doc.text);
      });
      if (data.quiz) {
        var questions = data.quiz.questions.map(function (question) { return question.q; }).join(" ");
        add("#ch/" + chapter.code + "/QUIZ", chapter.code + " " + chapter.title + " — Quiz", questions);
      }
    });
    D.general.forEach(function (doc) { add("#doc/" + encodeURIComponent(doc.id), doc.label, doc.text); });
    D.sheets.forEach(function (doc, index) { add("#fiches/" + index, doc.label, doc.text); });
    practiceUnits().forEach(function (unit) { add(practiceURL(unit), unit.title, unit.text); });
    hits.sort(function (a, b) { return b.score - a.score; });
    main.innerHTML = '<p class="crumbs"><a href="#bibliotheque">Bibliothèque</a></p><h1>Résultats de recherche</h1>' +
      searchForm(query) + '<p>' + (hits.length ? hits.length + ' résultat(s)' : 'Aucun résultat. Essayez un autre mot ou le nom anglais de la commande.') +
      '</p><div id="searchHits"></div><button class="btn" type="button" id="moreHits">Afficher plus de résultats</button>';
    bindSearch();
    var list = document.getElementById("searchHits");
    var more = document.getElementById("moreHits");
    var shown = 0;
    function showMore(fromButton) {
      var batch = hits.slice(shown, shown + 30);
      list.insertAdjacentHTML("beforeend", batch.map(function (hit) {
        return '<div class="hit"><a href="' + hit.href + '">' + esc(hit.title) + '</a><br><small>… ' + esc(hit.snippet) + ' …</small></div>';
      }).join(""));
      if (fromButton && batch.length) list.querySelectorAll(".hit a")[shown].focus();
      shown += batch.length;
      more.hidden = shown >= hits.length;
    }
    more.addEventListener("click", function () { showMore(true); });
    showMore(false);
  }

  function route() {
    var h;
    try { h = decodeURIComponent(location.hash.slice(1)).split("/"); }
    catch (e) { h = []; }
    var anchor;
    nav.classList.remove("open");
    if (h[0] === "ch") {
      chapter(h[1], h[2]);
      anchor = h[3];
    }
    else if (h[0] === "atelier") practice(h[1], h[2]);
    else if (h[0] === "doc") {
      var doc = h.slice(1);
      if (doc.length > 1 && /\.md$/.test(doc[doc.length - 2])) anchor = doc.pop();
      docPage(doc.join("/"));
    }
    else if (h[0] === "fiches") { sheets(h[1]); anchor = h[1] ? "fiche-" + h[1] : undefined; }
    else if (h[0] === "parcours") beginner();
    else if (h[0] === "bibliotheque") library();
    else if (h[0] === "recherche") search(h.slice(1).join("/"));
    else if (h[0] === "favoris") favorites();
    else home();
    var heading = anchor && document.getElementById(anchor);
    if (heading && main.contains(heading)) {
      heading.focus({ preventScroll: true });
      heading.scrollIntoView();
    } else {
      main.focus(); window.scrollTo(0, 0);
    }
  }

  document.getElementById("globalSearch").addEventListener("submit", function (event) {
    event.preventDefault();
    openSearch(document.getElementById("q").value);
  });
  document.getElementById("menuBtn").onclick = function () { nav.classList.toggle("open"); };
  window.addEventListener("hashchange", route);
  buildNav(); badge(); route();
})();
