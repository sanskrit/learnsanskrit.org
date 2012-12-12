data = LSO.d3.keyvalue({
    "a": 716,
    "e": 201,
    "i": 185,
    "u": 185,
    "A": 178,
    "I": 16,
    "f": 11,
    "o": 5,
    "E": 5,
    "U": 4,
    "O": 1
});

var bubbles = LSO.d3.bubbleGraph(data);
bubbles('#vowel-distribution');