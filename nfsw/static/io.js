document.addEventListener('DOMContentLoaded', function() {
    /**
     * Handling for sending commands to server.
     */
    window.qip = false;  // query in prograss flag.
    function query(q) {
        if (window.qip || window.iip) {
            return window.setTimeout(query, 10, q);
        }
        window.qip = true;

        var qipoff = function() {
            window.qip = false;
            ioconsole.autoScroll = true;
        };
        var spit = function(response) {
            var gdg = 'Oops! getting gobbledygook from server';

            var r;
            try {
                r = JSON.parse(response);
            } catch (e) {
                return barfslow(gdg, 'error', qipoff);
            }

            if (typeof r !== 'object') {
                return barf(gdg);
            }

            if (!('ans' in r)) {
                return barfslow(
                    'No answer from server!',
                    'error',
                    qipoff
                );
            }

            if ('reset' in r && r.reset) {
                return window.location.reload();
            }

            return barfslow(r.ans, 'concierge', qipoff);
        };

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/io/query', true);

        xhr.onreadystatechange = function() {
            if (this.readyState != 4) {
                return;
            }

            if (this.status == 200) {
                return spit(this.responseText);
            } else {
                return barfslow(
                    '💥', 'error', qipoff
                );
            }
        };
        xhr.send(q);
    }

    window.iip = false;
    function intro() {
        if (window.qip) {
            return window.setTimeout(intro, 10);
        }
        window.iip = true;

        var iipoff = function() {
            window.iip = false;
            ioconsole.autoScroll = true;
        };
        var spit = function(response, status) {
            var r;
            try {
                r = JSON.parse(response);
            } catch (e) {
                return barfslow('💥God is busy sodomizing the waitress.' +
                                '\nTry refreshing the page.', 'error', iipoff);
            }

            if (!('intro' in r)) {
                return barfslow(
                    '💥Too bad Dr. Gonad Dick is ' +
                    '\ntoo busy whipping his eggplant.' +
                    '\nTry refreshing the page.',
                    'error',
                    iipoff
                );
            }

            if (status == 200) {
                barfslow(r.intro, 'concierge', iipoff);
            } else {
                barfslow(r.intro, 'error', iipoff);
            }
        };

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/io/intro', true);

        xhr.onreadystatechange = function() {
            if (this.readyState != 4) {
                return;
            }

            if ([200, 500].indexOf(this.status) >= 0) {
                return spit(this.responseText, this.status);
            } else {
                return barfslow(
                    '💥God just fucked a skunk.' +
                    '\nTry refreshing the page.',
                    'error',
                    iipoff
                );
            }
        };
        xhr.send();
    }

    /**
     * Handling for console.
     */
    function barf(txt, type, p) {
        if (txt.length < 1) {
            return '';
        }
        barfblank();

        p = document.createElement('pre');
        p.className = type;

        p.append(txt);

        ioconsole.appendChild(p);

        return '';
    }
    function barfblank() {
        p = document.createElement('pre');
        p.className = 'blank';

        p.innerHTML = '\n';

        ioconsole.appendChild(p);
    }
    function barfslow(txt, type, cb, p) {
        if (!txt || txt.length < 1) {
            if (cb)
                cb();

            return '';
        }

        if (!p)
            barfblank();
        if (!p) {
            p = document.createElement('pre');
            p.className = type;

            ioconsole.appendChild(p);
        }
        p.append(txt.substring(0, 1));

        if (ioconsole.autoScroll) {
            p.scrollIntoView(false);
        }


        window.setTimeout(
            barfslow, 25,
            txt.substring(1, txt.length),
            type,
            cb,
            p
        );

        return '';
    }
    var ioconsole = document.getElementsByClassName('console')[0];
    ioconsole.onscroll = function(e) {
        if (!window.qip && !window.iip) {
            return;
        }

        if (e.target.scrollTop < e.target.lastScrollTop) {
            e.target.autoScroll = false;
        }

        e.target.lastScrollTop = e.target.scrollTop;
    };
    ioconsole.lastScrollTop = ioconsole.scrollTop;
    ioconsole.autoScroll = true;


    /**
     * Handling for the prompt.
     */
    function submit(e) {
        e.preventDefault();

        var input = e.target.querySelector('input');

        var cmd = input.value;
        if (cmd.length < 1)
            return;

        /**
         * Reset prompt.
         */
        input.value = '';

        /**
         * Send command to server.
         */
        query(cmd);
    }
    var form = document.querySelector('form');
    form.onsubmit = submit;

    intro();
});
