/**
 * Updates the object with the right color for
 * the percentage map.
 */
function updateObject(geoId, type, result) {
  d3.select(`#${type}_${geoId}`)
    .attr('fill', getColorScale()(result.yes_percent))
    .attr('title', result.yes_percent);
}

/**
 * Returns a colormap that goes from red to white to green
 **/
function getColorScale() {
  if (!window.colorScale) {
    window.colorScale = d3.scaleLinear()
    .range(["#DD0000", "#FFFFFF", "#0000DD"])
    .domain([20, 50, 80]);
  }

  return window.colorScale;
}

/**
 * Applies the results to the dom
 **/
function applyResults(data, type) {
  Object.values(data).forEach((obj) => {
    updateObject(obj.geo_id, type, obj);
  });
}


/**
 * Fetches the latest results for the given id and
 * updates the colors of the cantons in the dom.
 **/
async function updateCantons(votationId, vm) {
  return fetch(`/votes/json/${votationId}/`, {
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(response => response.json())
    .then(json => {
      applyResults(json, 'kanton');
      vm.canton_json = json;
    });
}

async function updateAllCommunes(votationId, vm) {
  return fetch(`/votes/json/${votationId}/communes/`, {
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(response => response.json())
    .then(json => {
      vm.commune_json = json;
      applyResults(json, 'commune');
    });
}
