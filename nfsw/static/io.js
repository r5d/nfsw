document.addEventListener('DOMContentLoaded', () => {
    /**
     * Handling for sending commands to server.
     */
    window.qip = false;  // query in prograss flag.
    function query(q) {
        if (window.qip) {
            return window.setTimeout(query, 10, q)
        }
        window.qip = true

        var qipoff = function() {
            window.qip = false
        }
        var spit = function(response) {
            var gdg = 'Oops! getting gobbledygook from server'

            var r
            try {
                r = JSON.parse(response)
            } catch (e) {
                return barfslow(gdg, 'error', qipoff)
            }

            if (!(typeof r === 'object')) {
                return barf(gdg)
            }

            if (!('ans' in r)) {
                return barfslow(
                    'No answer from server!',
                    'error',
                    qipoff
                )
            }

            return barfslow(r.ans, 'concierge', qipoff)
        }

        var xhr = new XMLHttpRequest()
        xhr.open('POST', '/io/query', true)

        xhr.onreadystatechange = function() {
            if (this.readyState != 4) {
                return
            }

            if (this.status == 200) {
                return spit(this.responseText)
            } else {
                return barfslow(
                    'Unable send command to server!', 'error', qipoff
                )
            }
        }
        xhr.send(q)
    }

    /**
     * Handling for console.
     */
    function barf(txt, type, p) {
        if (txt.length < 1) {
            return ''
        }
        barfblank()

        p = document.createElement('p')
        p.className = type

        p.append(txt)

        ioconsole.appendChild(p)

        return ''
    }
    function barfblank() {
        p = document.createElement('p')
        p.className = 'blank'

        p.innerHTML = '<br />'

        ioconsole.appendChild(p)
    }
    function barfslow(txt, type, cb, p) {
        if (txt.length < 1) {
            if (cb)
                cb()

            return ''
        }

        nl = false
        if (txt.charAt(0) == '\n')
            nl = true

        if (!p)
            barfblank()
        if (!p || nl) {
            p = document.createElement('p')
            p.className = type

            ioconsole.appendChild(p)
        }
        p.append(txt.substring(0, 1))
        p.scrollIntoView()

        window.setTimeout(
            barfslow, 0,
            txt.substring(1, txt.length),
            type,
            cb,
            p
        )

        return ''
    }
    var ioconsole = document.getElementsByClassName('console')[0]


    /**
     * Handling for the prompt.
     */
    function submit(e) {
        e.preventDefault()

        var input = e.target.querySelector('input')

        var cmd = input.value
        if (cmd.length < 1)
            return

        /**
         * Reset prompt.
         */
        input.value = ''

        /**
         * Send command to server.
         */
        query(cmd)
    }
    var form = document.querySelector('form')
    form.onsubmit = submit

})
