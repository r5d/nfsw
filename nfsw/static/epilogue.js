/**
 * SPDX-License-Identifier: ISC
 *
 * Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
 *
 * This file is part of nfsw.
 */

document.addEventListener('DOMContentLoaded', function() {
    var ep_wrapper = document.getElementsByClassName('epilogue-wrapper')[0];
    ep_wrapper.style = 'display:block';

    window.setTimeout(
        function() {
            window.location.href = "/io";
        }, 5000
    );
});
