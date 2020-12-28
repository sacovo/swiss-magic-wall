import {
  Component,
  EventEmitter,
  HostListener,
  OnInit,
  Output,
} from '@angular/core'
import * as topojson from 'topojson-client'
import { Topology } from 'topojson-specification'
import * as d3 from 'd3'
import { ScaleLinear } from 'd3'
import { Result } from '../votation'
import { TopoService } from '../topo.service'

function getHeight(width: number, topoJson: any): number {
  const [minX, minY, maxX, maxY] = topojson.bbox(topoJson)
  return ((maxY - minY) / (maxX - minX)) * width
}

function getProjection(width: number, topoJson: any) {
  const [minX, minY, maxX, maxY] = topojson.bbox(topoJson)
  const height = ((maxY - minY) / (maxX - minX)) * width

  const x = d3.scaleLinear().range([0, width]).domain([minX, maxX])

  const y = d3.scaleLinear().range([0, height]).domain([maxY, minY])

  return d3.geoTransform({
    point: function (px, py) {
      this.stream.point(x(px), y(py))
    },
  })
}

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.less'],
})
export class MapComponent implements OnInit {
  private svg: any

  private path: any

  private zoom = d3
    .zoom()
    .scaleExtent([0.8, 8])
    .on('zoom', (event) => this.zoomed(event))
  private width = 0
  private height = 0
  private topoJson: any
  fullWidth= false;

  hideCantons = false

  private colorScale: ScaleLinear<string, number, never>
  private g?: any

  private cantonId: number = 0

  @Output() mapUpdated = new EventEmitter()
  @Output() cantonSelect = new EventEmitter()
  @Output() communeSelect = new EventEmitter()

  constructor(private topoService: TopoService) {
    this.colorScale = d3
      .scaleLinear<string, number, never>()
      .range(['#FF0000', '#FFFFFF', '#0000FF'])
      .domain([0.2, 0.5, 0.8])
  }

  ngOnInit(): void {
    this.createMap()
  }

  appendFeatures(geo: any, cssClass: string, clicked?: any) {
    var g = this.g.append('g')

    g.selectAll('path')
      .data(geo.features)
      .enter()
      .append('path')
      .attr('cursor', clicked ? 'pointer' : 'default')
      .attr('id', function (d: any) {
        if (d.properties.vogenr) {
          return `${cssClass}_${d.properties.vogenr}`
        }
        return `${cssClass}_${d.properties.id}`
      })
      .attr('class', cssClass)
      .attr('fill', '#fff')
      .on('click', clicked)
      .attr('d', this.path)

    return g
  }

  loadTopoJson(): void {
    this.topoService.getTopoData().then((json: any) => {
      this.topoJson = json as Topology
      this.drawMap()
    })
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    this.drawMap()
  }

  drawMap() {
    this.width = window.innerWidth < 900 ? window.innerWidth : window.innerWidth - 200
    this.height = getHeight(this.width, this.topoJson)
    const maxHeight = window.innerHeight - 38

    if (this.height > maxHeight) {
      this.width = this.width * (maxHeight / this.height)
      this.height = maxHeight
    }

    this.path = d3.geoPath(getProjection(this.width, this.topoJson))

    const root = d3.select('#map')
    root.html('')

    let latestTap = 0

    this.svg = root
      .append('svg')
      .attr('viewbox', `0 0 ${window.innerWidth} ${maxHeight}`)
      .attr('width', window.innerWidth)
      .attr('height', maxHeight)
      .attr('preserveAspectRatio', 'xMinYMin meet')
      .attr('version', '1.1')
      .on('dblclick', () => this.reset())
      .on('touchstart', (event: any) => {
        const timeSince = event.timeStamp - latestTap
        if (timeSince < 600) {
          event.preventDefault()
          this.reset()
        }
        latestTap = event.timeStamp
      })
    this.g = this.svg.append('g').attr('id', 'mapRoot')

    this.svg.call(this.zoom).on('dblclick.zoom', null)

    this.appendFeatures(topojson.feature(this.topoJson, this.topoJson.objects.K4suis_18480101_gf), "switzerland")

    this.appendFeatures(
      topojson.feature(this.topoJson, this.topoJson.objects.K4voge_20201018_gf),
      'commune',
      (event: any, obj: any) => this.communeSelect.emit(obj)
    )
    this.appendFeatures(
      topojson.feature(this.topoJson, this.topoJson.objects.K4seen_yyymmdd11),
      'see'
    )
    this.appendFeatures(
      topojson.feature(this.topoJson, this.topoJson.objects.K4kant_19970101_gf),
      'kanton',
      (event: any, obj: any) => {
        event.stopPropagation()
        this.selectCaton(obj)
        d3.pointer(event, this.svg.node())
      }
    )
    this.mapUpdated.emit()
  }

  createMap(): void {
    this.loadTopoJson()
  }

  reset() {
    this.svg
      .transition()
      .duration(400)
      .call(
        this.zoom.transform,
        d3.zoomIdentity,
        d3
          .zoomTransform(this.svg.node())
          .invert([this.width / 2, this.height / 2])
      )
    this.g.selectAll(`.kanton`).attr('data-active', 'false')
    this.cantonId = 0
    this.cantonSelect.emit(null)
  }

  zoomed(event: any) {
    const { transform } = event
    this.g.attr('transform', transform)
    //this.g.attr('stroke-width', 1 / transform.k)
  }

  selectCaton(obj: any) {
    const [[x0, y0], [x1, y1]] = this.path.bounds(obj)

    this.svg
      .transition()
      .duration(400)
      .call(
        this.zoom.transform,
        d3.zoomIdentity
          .translate(this.width / 2, this.height / 2)
          .scale(
            Math.min(
              8,
              0.9 / Math.max((x1 - x0) / this.width, (y1 - y0) / this.height)
            )
          )
          .translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
      )
    this.cantonId = obj.properties.id
    this.cantonSelect.emit(obj)
    this.g.selectAll(`.kanton`).attr('data-active', 'false')
    this.g.select(`#kanton_${obj.properties.id}`).attr('data-active', 'true')
  }

  updateObject(
    geoId: number,
    type: string,
    result: number,
    is_final: boolean
  ): void {
    if (this.svg && !isNaN(result)) {
      this.svg
        .select(`#${type}_${geoId}`)
        .attr('fill', this.colorScale(result))
        .attr('state', is_final ? 'final' : 'predicted')
    }
  }

  applyResults(data: Result[], type: string) {
    Object.values(data).forEach((obj) => {
      this.updateObject(
        obj.geo_id,
        type,
        obj.yes_total / (obj.yes_total + obj.no_total),
        obj.is_final
      )
    })
  }

  updateCantons(data: Result[]) {
    this.applyResults(data, 'kanton')
  }

  updateCommunes(data: Result[]) {
    this.applyResults(data, 'commune')
  }

  cantonImage(): string | undefined {
    return `/assets/cantons/${this.cantonId}.svg`
  }

  toggleCanton(event: any) {
    this.hideCantons = !this.hideCantons
  }
}
