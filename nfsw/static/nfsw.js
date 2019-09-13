window.nfsw = {
    fErr: function(msg) {
        $('.msg-block .content p').empty().text(msg);
        $('.msg-block .content').addClass('error');
        $('.msg-block').show();
    },
    fInfo: function(msg) {
        $('.msg-block .content p').empty().text(msg);
        $('.msg-block .content').addClass('info');
        $('.msg-block').show();
    },
    fFormInit: function() {
        var root = this;

        $('form.auth').submit(function(ev) {
            ev.preventDefault();

            root.fFormPost($(this).serialize());
        });
    },
    fFormPost: function(post) {
        var root = this;

        $.post('/auth/start', post)
         .done(function(data, status, xhr) {
             if (!'status' in data) {
                 root.fErr('Unable to log you in!');
             }
             var status = data['status'];

             if (status == 'pass') {
                 return root.fFormAskPass(data['msg']);
             }
             if (status == 'error') {
                 return root.fFormError(data);
             }
             if (status == 'ok') {
                 return root.fFormPostOk(data);
             }

             root.fErr('Unknow error. Unable to log you in!');
         })
         .fail(function(xhr, status, err) {
             console.log([xhr,status, err])
         });
    },
    fFormAskPass: function(msg) {
        var root = this;

        root.fInfo(msg);

        $('input[type=password]').prop('disabled', false);
        //$('input[type=password]').prop('required', true);
        $('.auth-pass').show();
    },
    fFormError: function(data) {
        var root = this;

        root.fErr(data['msg']);
        if (!('fields' in data)) {
            return;
        }

        $.each(data['fields'], function(i, f) {
            $('form .' + f).addClass('error');
        });
    },
    fFormPostOk: function(data) {
        if (!('url' in data)) {
            root.fErr('Unable to redirect!')
        }

        window.location.href = data.url;
    },

    fInit: function(options) {
        var root = this;

        console.log('Initing nfsw...');

        root.fFormInit();
    },
}

$(document).ready(function() {
    window.nfsw.fInit({});
});
