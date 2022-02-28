(function(ns) {

    // Scheme data. This is split into separate objects below.
    // Sorted by code point.
    var SCHEMES = [
        ['bengali', 0x0980],
        ['devanagari', 0x0900],
        ['gujarati', 0x0a80],
        ['gurmukhi', 0x0a00],
        ['kannada', 0x0c80],
        ['malayalam', 0x0d00],
        ['oriya', 0x0b00],
        ['tamil', 0x0b80],
        ['telugu', 0x0c00],
        ['hk', null],
        ['iast', null],
        ['itrans', null],
        ['kolkata', null],
        ['slp1', null],
        ['velthuis', null],
    ],

    // Start of the Devanagari block.
    BRAHMIC_FIRST_CODE_POINT = 0x0900,

    // End of the Malayalam block.
    BRAHMIC_LAST_CODE_POINT = 0x0d7f,

    // Schemes sorted by Unicode code point. Ignore schemes with none defined.
    BLOCKS = SCHEMES
        .filter(function(x) { return x[1]; })  // keep non-null
        .sort(function(x, y) { return y[1] - x[1]; });  // sort by code point

    // Match on special Roman characters
    var RE_IAST_OR_KOLKATA_ONLY = /[āīūṛṝḷḹēōṃḥṅñṭḍṇśṣḻ]/,

    // Match on chars shared by ITRANS and Velthuis
    RE_ITRANS_OR_VELTHUIS_ONLY = /aa|ii|uu|~n/,

    // Match on ITRANS-only
    RE_ITRANS_ONLY = /ee|oo|\^[iI]|RR[iI]|L[iI]|~N|N\^|Ch|chh|JN|sh|Sh|\.a/,

    // Match on Kolkata-specific Roman characters
    RE_KOLKATA_ONLY = /[ēō]/,

    // Match on SLP1-only characters and bigrams
    RE_SLP1_ONLY = RegExp(['[fFxXEOCYwWqQPB]|kz|Nk|Ng|tT|dD|Sc|Sn|',
                           '[aAiIuUfFxXeEoO]R|',
                           'G[yr]|(\\W|^)G'].join('')),

    // Match on Velthuis-only characters
    RE_VELTHUIS_ONLY = /\.[mhnrlntds]|"n|~s/;

    var Scheme = ns.Scheme = {};
    for (i = 0; i < SCHEMES.length; i++) {
        var value = SCHEMES[i][0];
        Scheme[value] = value;
    }

    ns.detect = function(text) {
        // Brahmic schemes are all within a specific range of code points.
        for (var i = 0; i < text.length; i++) {
            var L = text[i],
                code = L.charCodeAt(L);
            if (code >= BRAHMIC_FIRST_CODE_POINT && code <= BRAHMIC_LAST_CODE_POINT) {
                for (var j = 0; j < BLOCKS.length; j++) {
                    var block = BLOCKS[j];
                    if (code >= block[1]) {
                        return block[0];
                    }
                }
            }
        }

        // Romanizations
        if (RE_IAST_OR_KOLKATA_ONLY.test(text)) {
            if (RE_KOLKATA_ONLY.test(text)) {
                return Scheme.kolkata;
            }
            return Scheme.iast;
        }

        if (RE_ITRANS_ONLY.test(text)) {
            return Scheme.itrans;
        }

        if (RE_SLP1_ONLY.test(text)) {
            return Scheme.slp1;
        }

        if (RE_VELTHUIS_ONLY.test(text)) {
            return Scheme.velthuis;
        }

        if (RE_ITRANS_OR_VELTHUIS_ONLY.test(text)) {
            return Scheme.itrans;
        }

        return Scheme.hk;
    };

}(window.sanskrit = window.sanskrit || {}));
