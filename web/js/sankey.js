var visual = {
  units: 'CHF',
  valueRange: [1, 100000000],
  innerHeight: 650,
  scaleWidth: 60,
  scaleMax: 300
};

(function($) {
  visual.drawSankey = function() {
    var nodeDesc = {
        0:'<h3>Disparitätenabbau (#)</h3>Der Disparitätenabbau mildert die unterschiedliche finanzielle Leistungsfähigkeit der Gemeinden. Er wird durch die Gemeinden finanziert. Gemeinden mit einem harmonisierten Steuerertragsindex (HEI) grösser als 100 erbringen eine Ausgleichsleistung, Gemeinden mit einem HEI kleiner als 100 erhalten einen Zuschuss. Mehr zum Thema siehe Erklärungen-Button.',
        1:'<h3>Mindestausstattung (#)</h3>Die Mindestausstattung bezweckt, den finanzschwächsten Gemeinden ausreichende Mittel zu verschaffen, damit sie ihre Aufgaben wirtschaftlich und sparsam erfüllen können. Mehr zum Thema siehe Erklärungen-Button.',
        2:'<h3>Pauschale Abgeltung (#)</h3>Die Gemeinden Bern, Biel und Thun erhalten zur teilweisen Abgeltung ihrer überdurchschnittlich hohen Zentrumslasten in den Aufgabenbereichen privater Verkehr, öffentliche Sicherheit, Gästeinfrastruktur, Sport und soziale Sicherheit einen jährlichen Zuschuss. Mehr zum Thema siehe Erklärungen-Button.',
        3:'<h3>Übermässige, geografisch-topografische Lasten (#)</h3>Einer Gemeinde können aus ihrer geografischen Lage oder aufgrund struktureller Umstände Nachteile erwachsen. Das FILAG setzt für die gezielte Entlastung zwei Zuschüsse ein: 1) Zuschuss Fläche und 2) Zuschuss Strassenlänge. Mehr zum Thema siehe Erklärungen-Button.',
        4:'<h3>Übermässige, sozio-demografische Lasten (#)</h3>Gemeinden, die aufgrund ihrer sozio-demografischen Situation belastet sind, erhalten jährlich einen Zuschuss. Dieser dient u.a. zur Abfederung des Selbstbehaltes bei verschiedenen Angeboten der institutionellen Sozialhilfe. Mehr zum Thema siehe Erklärungen-Button.'
    };

    var chart = $('#chart'),
        margin = {top: 20, right: 20, bottom: 20, left: 20},
        width = chart.width() - margin.left - margin.right - visual.scaleWidth - 5,
        height = visual.innerHeight - margin.top - margin.bottom;

    var formatNumber = d3.format(',.0f'),
        format = function(d) { return formatNumber(d) + ' ' + visual.units; },
        nodeClass = function(d) {
          return 'node ' + d.side + ' node_' + d.node;
        },
        linkClass = function(d) {
          return 'link ' + 'node_' + d.source.node + ' node_' + d.target.node;
        };

    var colorScaleRed = d3.scale.quantize()
            .domain(visual.valueRange)
            .range(colorbrewer.Reds[6]),
        colorScaleGrey = d3.scale.quantize()
            .domain(visual.valueRange)
            .range(colorbrewer.Greys[4]),
        colorScaleGreen = d3.scale.quantize()
            .domain(visual.valueRange)
            .range(colorbrewer.Greens[6]);

    var colors =  {left: colorScaleRed, container: colorScaleGrey, right: colorScaleGreen};

    var nodeColor = function(d){
        return colors[d.side](d.value);
    };

    var svg = d3.select('#chart').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform',
              'translate(' + margin.left + ',' + margin.top + ')');

    var sankey = d3.sankey()
        .nodeWidth(36)
        .nodePadding(10)
        .size([width, height]);

    var path = sankey.link();

    d3.json('data/2012.json', function(error, graph) {
      sankey
          .nodes(graph.nodes)
          .links(graph.links)
          .layout(32);

      var link = svg.append('g').selectAll('.link')
          .data(graph.links)
          .enter().append('path')
          .attr('class', linkClass)
          .attr('d', path)
          .style('stroke-width', function(d) { return Math.max(1, d.dy); })
          .sort(function(a, b) { return b.dy - a.dy; });

      link.attr('data-tooltip', function(d) {
            return '<strong>' + format(d.value) + '</strong><br />' +
                   d.source.name + ' &rarr; ' + d.target.name;
      });
      utils.tooltip(chart.find('path.link'));

      var node = svg.append('g').selectAll('.node')
          .data(graph.nodes)
          .enter().append('g')
          .attr('class', nodeClass)
          .attr('transform', function(d) {
              return 'translate(' + d.x + ',' + d.y + ')'; });

      node.append('rect')
          .attr('height', function(d) { return d.dy; })
          .attr('width', sankey.nodeWidth())
          .style('fill', function(d) {
              d.color = nodeColor(d);
              return d.color;
          })
          .style('stroke', function(d) {
              return d3.rgb(d.color).darker(0.3); })
          .attr('data-tooltip', function(d){
              if (d.node in nodeDesc){
                  return nodeDesc[d.node].replace('#', format(d.value));
              }
              return '<strong>'+ d.name + '</strong><br />' + format(d.value);
          });

      utils.tooltip(chart.find('.node rect'));

      node.append('text')
          .attr('x', -6)
          .attr('y', function(d) { return d.dy / 2; })
          .attr('dy', '.35em')
          .attr('text-anchor', 'end')
          .attr('transform', null)
          .text(function(d) { return d.name; })
          .filter(function(d) { return d.x < width / 2; })
          .attr('x', 6 + sankey.nodeWidth())
          .attr('text-anchor', 'start');
    });
  };

  visual.drawScale = function() {
    var height = visual.innerHeight - 40;
    var scaleMillion = height / visual.scaleMax;

    var svg = d3.select('#chart').append('svg')
      .attr('width', visual.scaleWidth)
      .attr('height', visual.innerHeight)
      .append('g')
      .attr('transform', 'translate(0,20)');

    svg.append('line')
      .attr('x1', 0)
      .attr('y1', 0)
      .attr('x2', 0)
      .attr('y2', height);

    svg.append('line')
      .attr('x1', 0)
      .attr('y1', 0)
      .attr('x2', 18)
      .attr('y2', 0);

    svg.append('line')
      .attr('x1', 0)
      .attr('y1', height)
      .attr('x2', 18)
      .attr('y2', height);

    svg.append('text')
      .attr('x', 5)
      .attr('y', 15)
      .attr('dy', '.35em')
      .attr('text-anchor', 'end')
      .text('Mio. CHF')
      .attr('text-anchor', 'start');

    $(Array(10, 50, 100, 200)).each(function() {
      svg.append('line')
        .attr('x1', 0)
        .attr('y1', height - scaleMillion * this)
        .attr('x2', 7)
        .attr('y2', height - scaleMillion * this);

      svg.append('text')
          .attr('x', 15)
          .attr('y', height - scaleMillion * this)
          .attr('dy', '.35em')
          .attr('text-anchor', 'end')
          .text(this)
          .attr('text-anchor', 'start');
      });
  };
}(jQuery));