(function(LSO) {
    /**
     * Convert the given string to a valid ID.
     */
    LSO.toID = function(s) {
        return s.toLowerCase().replace(/[\s]/g, '-').replace(/[:;,.!()"]/g, '');
    };

    /**
     * Transliterate to the "main" Sanskrit scheme.
     */
    LSO.sa1 = function(text, from) {
        from = from || 'slp1';
        return Sanscript.t(text, from, LSO.settings.get('sa1'));
    };

    /**
     * Transliterate to the "secondary" Sanskrit scheme.
     */
    LSO.sa2 = function(text, from) {
        from = from || 'slp1';
        return Sanscript.t(text, from, LSO.settings.get('sa2'));
    };
}(LSO = window.LSO || {}));