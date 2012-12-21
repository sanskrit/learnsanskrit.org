(function(ns) {
    ns.d3 = ns.d3 || {};
    ns = ns.d3;

    var makeSVG = function(selector, width, height, margin) {
        margin = margin || { left: 0, right: 0, top: 0, bottom: 0 };
        var svg = d3.select(selector).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        return svg;
    };

    function accessor(my, options, name) {
        return function(_) {
            if (!arguments.length) return options[name];
            options[name] = _;
            return my;
        };
    }

    function obj_accessor(my, options, name) {
        return function(_) {
            if (!arguments.length) return options[name];
            for (var key in _) {
                if (_.hasOwnProperty(key)) {
                    options[name][key] = _[key];
                }
            }
            return my;
        };
    }

    ns.pieChart = function(data) {
        var width = 400,
            height = 400,
            showLegend = false,
            x = function(d) { return d.key; },
            y = function(d) { return d.value; },
            text = function(d) { return x(d.data); };

        function my(selector) {
                radius = Math.min(width, height) / 2;

            var color = d3.scale.category20c();

            var arc = d3.svg.arc()
                .outerRadius(radius)
                .innerRadius(radius/1.6);

            var pie = d3.layout.pie()
                .sort(null)
                .value(y);

            var svg = d3.select(selector).append("svg")
                .attr("width", width)
                .attr("height", height)
              .append("g")
                .attr("transform", "translate(" + radius + "," + radius + ")");

              var g = svg.selectAll(".arc")
                  .data(pie(data))
                .enter().append("g")
                  .attr("class", "arc");

              g.append("path")
                  .attr("d", arc)
                  .style("fill", function(d, i) { return color(y(d.data)); });

            if (showLegend) {
                var h = 20,
                    legendHeight = h * data.length,
                    boxSize = h - 2,
                    legend = svg.append("g")
                    .attr("class", "legend")
                    .attr("width", width / 2)
                    .attr("height", legendHeight)
                    .attr("transform", "translate(" + width/2 + "," + -legendHeight/2 + ")")
                  .selectAll("g")
                    .data(data)
                .enter().append("g")
                    .attr("transform", function(d, i) { return "translate(0," + i * h + ")"; });

                legend.append("rect")
                    .attr("width", boxSize)
                    .attr("height", boxSize)
                    .style("fill", function(d) { return color(d.value); });

                legend.append("text")
                    .attr("x", boxSize + 6)
                    .attr("y", boxSize / 2)
                    .attr("dy", ".35em")
                    .text(text);
            }
        }

        my.height = function(_) {
            if (!arguments.length) return height;
            height = _;
            return my;
        };
        my.data = function(_) {
            if (!arguments.length) return data;
            data = _;
            return my;
        };
        my.showLegend = function(_) {
            if (!arguments.length) return showLegend;
            showLegend = _;
            return my;
        };
        my.text = function(_) {
            if (!arguments.length) return text;
            text = _;
            return my;
        };
        my.width = function(_) {
            if (!arguments.length) return width;
            width = _;
            return my;
        };
        my.x = function(_) {
            if (!arguments.length) return x;
            x = _;
            return my;
        };
        my.y = function(_) {
            if (!arguments.length) return y;
            y = _;
            return my;
        };

        return my;
    };

    ns.keyvalue = function(data) {
        returned = [];
        for (var k in data) {
            if (data.hasOwnProperty(k)) {
                returned.push({ key: k, value: data[k] });
            }
        }
        return returned;
    };

    ns.barGraph = function() {
        var margin = {top: 50, right: 50, bottom: 50, left: 50},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom,
            data;

        function my(selector) {

            var formatPercent = d3.format(".0%");

            var x = d3.scale.ordinal()
                .rangeRoundBands([0, width], 0.1);

            var y = d3.scale.linear()
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

            var svg = d3.select(selector).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            x.domain(data.map(function(d) { return d.key; }));
            y.domain([0, d3.max(data, function(d) { return d.value; })]);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
              .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Frequency");

            svg.selectAll(".bar")
                .data(data)
              .enter().append("rect")
                .attr("class", "bar")
                .attr("x", function(d) { return x(d.key); })
                .attr("width", x.rangeBand())
                .attr("y", function(d) { return y(d.value); })
                .attr("height", function(d) { return height - y(d.value); });
        }
        my.data = function(value) {
            if (!arguments.length) return data;
            data = value;
            return my;
        };

        return my;
    };

    ns.bubbleChart = function(data) {
        function my(selector) {
            var diameter = 480,
                format = d3.format(",d"),
                color = d3.scale.category20c();

            var bubble = d3.layout.pack()
                .sort(null)
                .size([diameter, diameter])
                .padding(20);

            var svg = d3.select(selector).append("svg")
                .attr("width", diameter)
                .attr("height", diameter)
                .attr("class", "bubble");

            var node = svg.selectAll(".node")
              .data(bubble.nodes({children: data})
              .filter(function(d) { return !d.children; }))
            .enter().append("g")
              .attr("class", "node")
              .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

            node.append("circle")
              .attr("r", function(d) { return d.r; })
              .style("fill", function(d) { return color(d.key); });

            node.append("text")
              .text(function(d) { return LSO.sa1(d.key); })
              .attr("dy", function(d) { return d.r / 4; })
              .style("font-size", function(d) { return d.r; })
              .style("text-anchor", "middle");

            node.append("title")
              .text(function(d) { return LSO.sa2(d.key) + ": " + format(d.value); });
        }

        return my;
    };

    ns.tree = function(data) {
        var options = {
            width: 400,
            height: 600,
            margin: {top: 50, right: 150, bottom: 50, left: 50}
        };

        function my(selector) {
            var width = options.width,
                height = options.height,
                margin = options.margin;
            var svg = makeSVG(selector, width, height, margin)
                .attr('class', 'tree');

            var tree = d3.layout.tree()
                .sort(null)
                .size([height, width]);

            var nodeData = tree.nodes(data),
                linkData = tree.links(nodeData);

            var diagonal = d3.svg.diagonal()
                .projection(function(d) {
                    return [d.y, d.x];
                });

            var links = svg.selectAll('path.link')
                .data(linkData)
                .enter()
                .append('path')
                .attr('class', 'link')
                .attr('d', diagonal);

            var nodes = svg.selectAll('g.node')
                .data(nodeData)
                .enter()
                .append('g')
                .attr('class', 'node')
                .attr('transform', function(d) {
                    return "translate(" + d.y + "," + d.x + ")";
                });

            nodes.append('circle')
                .attr('r', '5');

            nodes.append('text')
                .attr('class', 'sa1')
                .attr('dy', 7)
                .text(function(d) {
                    return Sanscript.t(d.name, 'hk', LSO.settings.get('sa1'));
                });
        }
        my.data = function(_) {
            if (!arguments.length) return data;
            data = _;
            return my;
        };
        my.height = accessor(my, options, 'height');
        my.margin = obj_accessor(my, options, 'margin');
        my.width = accessor(my, options, 'width');
        return my;
    };

    ns.formTree = function(data) {
        var my = ns.tree(data)
            .margin({top: 0, bottom: 0})
            .width(300);
        return my;
    };

}(LSO = window.LSO || {}));