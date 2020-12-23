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
  names_ready!: Promise<void>

  canton_names: any = {}

  constructor() {}

  getTopoData(): Promise<Topology> {
    if (!this.data) {
      this.data = d3.json('/assets/switzerland.json') as Promise<Topology>
      this.names_ready = this.data.then((topo: Topology) => {
        {
          const cantons = topojson.feature(
            topo,
            topo.objects.K4kant_19970101_gf
          ) as FeatureCollection
          cantons.features.forEach((canton) => {
            this.canton_names[canton.properties!.id] = canton.properties!.name
          })
        }
      })
    }
    return this.data
  }


  getCantonName(id: number): string {
    return this.canton_names[id]
  }
}
