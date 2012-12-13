$(function() {
    var data = LSO.d3.keyvalue({
        "1": 2820,
        "2": 1350,
        "6": 402,
        "7": 336,
        "3": 317,
        "8": 255,
        "5": 102,
        "4": 39
    });

    var chart = LSO.d3.pieChart(data)
        .width(600)
        .showLegend(true)
        .text(function(d) { return 'Case ' + d.key; });
    chart('#case-distribution');
}());