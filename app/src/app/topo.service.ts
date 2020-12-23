import { Injectable } from '@angular/core'
import { Topology } from 'topojson-specification'
import * as topojson from 'topojson-client'
import * as d3 from 'd3'
import { FeatureCollection } from 'geojson'

@Injectable({
  providedIn: 'root',
})
export class TopoService {
  data: Promise<Topology> | undefined = undefined

  names: any = {}

  constructor() {}

  getTopoData(): Promise<Topology> {
    if (!this.data) {
      this.data = d3.json('/assets/switzerland.json') as Promise<Topology>
      this.data.then((topo: Topology) => {
        const communes = topojson.feature(
          topo,
          topo.objects.K4voge_20201018_gf
        ) as FeatureCollection;
        communes.features.forEach((commune) => {
          this.names[commune.properties!.vogenr] = commune.properties!.vogename;
        })
      })
    }
    return this.data
  }

  getNameFor(id: number): string {
    return this.names[id] || id
  }
}
