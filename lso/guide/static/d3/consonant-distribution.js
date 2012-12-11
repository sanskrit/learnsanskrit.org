data = LSO.d3.keyvalue({
    'ta': 4074,
    'ra': 2987,
    'ya': 2877,
    'ma': 2775,
    'na': 2653,
    'va': 2349,
    'sa': 2102,
    'da': 1383,
    'ka': 1370,
    'pa': 1367,
    'za': 892,
    'ca': 838,
    'Sa': 766,
    'ha': 742,
    'bha': 719,
    'ja': 710,
    'ga': 653,
    'dha': 585,
    'Na': 454,
    'tha': 364,
    'la': 323,
    'ba': 271,
    'Ja': 270,
    'kha': 118,
    'Ta': 114,
    'Ga': 90,
    'cha': 79,
    'Tha': 49,
    'pha': 35,
    'gha': 33,
    'Dha': 33,
    'Da': 29,
    'jha': 1
});

var bubbles = LSO.d3.bubbleGraph(data);
bubbles('#consonant-distribution');