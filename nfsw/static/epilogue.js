document.addEventListener('DOMContentLoaded', function() {
    var ep_wrapper = document.getElementsByClassName('epilogue-wrapper')[0];
    ep_wrapper.style = 'display:block';

    window.setTimeout(
        function() {
            window.location.href = "/io";
        }, 5000
    );
});
