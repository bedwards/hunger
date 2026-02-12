(function () {
    'use strict';

    var NOVEL_KEY = 'hunger_novel_bookmark';
    var EXTRA_KEY = 'hunger_extra_bookmark';
    var ROMAN = ['I', 'II', 'III', 'IV'];

    function get(key) {
        try { return JSON.parse(localStorage.getItem(key)); }
        catch (e) { return null; }
    }

    function set(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    }

    function scrollPct() {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        return h > 0 ? window.scrollY / h : 0;
    }

    function scrollTo(pct) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        window.scrollTo(0, h * pct);
    }

    // --- Reading position tracking ---

    var main = document.querySelector('main');
    if (main && main.dataset.type && main.dataset.chapter) {
        var type = main.dataset.type;
        var chapter = parseInt(main.dataset.chapter, 10);
        var key = type === 'novel' ? NOVEL_KEY : EXTRA_KEY;

        // Debounced scroll save
        var timer;
        window.addEventListener('scroll', function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                set(key, { chapter: chapter, scroll: scrollPct() });
            }, 250);
        });

        // Save on leave
        window.addEventListener('beforeunload', function () {
            set(key, { chapter: chapter, scroll: scrollPct() });
        });

        // Restore position if same chapter
        var bm = get(key);
        if (bm && bm.chapter === chapter && bm.scroll > 0.01) {
            requestAnimationFrame(function () {
                setTimeout(function () { scrollTo(bm.scroll); }, 150);
            });
        }
    }

    // --- Home page bookmarks ---

    var novelEl = document.getElementById('novel-bookmark');
    var extraEl = document.getElementById('extra-bookmark');
    var noEl = document.getElementById('no-bookmarks');

    if (novelEl) {
        var nb = get(NOVEL_KEY);
        if (nb) {
            var pct = Math.round(nb.scroll * 100);
            novelEl.href = 'part-' + nb.chapter + '.html';
            novelEl.innerHTML = 'Continue reading: Part ' + ROMAN[nb.chapter - 1] +
                ' <span class="detail">(' + pct + '% through)</span>';
            novelEl.style.display = 'block';
        }
    }

    if (extraEl) {
        var eb = get(EXTRA_KEY);
        if (eb) {
            var pct2 = Math.round(eb.scroll * 100);
            extraEl.href = 'extra-' + eb.chapter + '.html';
            extraEl.innerHTML = 'Continue extras: Part ' + ROMAN[eb.chapter - 1] +
                ' companion <span class="detail">(' + pct2 + '% through)</span>';
            extraEl.style.display = 'block';
        }
    }

    if (noEl) {
        if (get(NOVEL_KEY) || get(EXTRA_KEY)) {
            noEl.style.display = 'none';
        }
    }
})();
