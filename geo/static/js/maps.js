function getHeight(width, topoJson) {
  const [minX, minY, maxX, maxY] = topojson.bbox(topoJson);
  return ((maxY - minY) / (maxX - minX)) * width;
}

function getProjection(width, topoJson) {
  const [minX, minY, maxX, maxY] = topojson.bbox(topoJson);
  const height = ((maxY - minY) / (maxX - minX)) * width;

  const x = d3.scaleLinear()
    .range([0, width])
    .domain([minX, maxX]);

  const y = d3.scaleLinear()
    .range([0, height])
    .domain([maxY, minY]);

  return d3.geoTransform({
    point: function(px, py) {
      this.stream.point(x(px), y(py));
    }
  });
}

function appendFeatures(svg, geo, path, cssClass, clicked) {
  var g = svg.append('g');

  g.selectAll('path')
    .data(geo.features)
    .enter()
    .append('path')
    .attr('cursor', clicked ? 'pointer' : 'default')
    .attr('id', function(d) { return `${cssClass}_${d.properties.id}`; })
    .attr("data-name", function(d) { return d.properties.name; })
    .attr('class', cssClass)
    .attr('fill', 'none')
    .on('click', clicked)
    .attr('d', path);

  return g;

}


function drawMap(root, app) {
  d3.json("/static/switzerland.json").then(function(topoJson) {

    const width = 1400;
    const height = getHeight(width, topoJson);
    const path = d3.geoPath(getProjection(width, topoJson));

    const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on("zoom", zoomed);

    const svg = root.append("svg")
      .attr("viewbox", `0 0 ${width} ${height}`)
      .attr("width", width)
      .attr("height", height)
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("version", "1.1")
      .on("dblclick", reset);


    const g = svg.append("g").attr('id', 'mapRoot');

    svg.call(zoom).on("dblclick.zoom", null);

    appendFeatures(g, topojson.feature(topoJson, topoJson.objects.K4voge_20200101_gf), path, 'commune', function(event, obj) {
      event.stopPropagation();
      app.selectCommune(obj.properties.id);
    });
    appendFeatures(g, topojson.feature(topoJson, topoJson.objects.K4seen_yyymmdd11), path, 'see');
    let gCantons = appendFeatures(
      g,
      topojson.feature(topoJson, topoJson.objects.K4kant_19970101_gf),
      path,
      'kanton',
      function(event, obj) {
        event.stopPropagation();
        root.attr('data-canton-id', obj.properties.id);
        app.selectCanton(obj.properties.id);

        root.node().dispatchEvent(new Event('mapChange'));

        d3.selectAll(`.kanton`).attr('data-active', 'false');
        d3.select(`#kanton_${obj.properties.id}`).attr('data-active', 'true');

        const [[x0, y0], [x1, y1] ] = path.bounds(obj);
        svg.transition().duration(750).call(
          zoom.transform,
          d3.zoomIdentity
          .translate(width / 2, height / 2)
          .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
          .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
          d3.pointer(event, svg.node())
        );
      }
    );

    function reset() {
      d3.selectAll(`.kanton`).attr('data-active', 'false');
      root.attr('data-canton-id', null);
      app.deselectCanton();

      root.node().dispatchEvent(new Event('mapChange'));
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity,
        d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
      );
    }

    function zoomed(event) {
      const {transform} = event;
      g.attr('transform', transform);
      g.attr('stroke-width', 1 / transform.k);
    }
  });


}
