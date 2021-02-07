import { CantonResult, CommuneResult } from '../votation'
import { TopoService } from '../topo.service'

export class CommuneEntry {
  name: string = ''
  yes_percent: number
  yes_total: number
  no_total: number
  participation: number
  final: boolean
  canton: string = ''

  constructor(source: CommuneResult, topoService: TopoService) {
    this.participation = source.participation
    this.yes_total = source.yes_total
    this.no_total = source.no_total
    this.yes_percent =
      (source.yes_total / (source.no_total + source.yes_total)) * 100
    this.final = source.is_final
    this.name = source.name
    topoService.names_ready?.then(() => {
      this.canton = topoService.getCantonName(source.canton)
    })
  }
}

export class CantonEntry {
  id: number
  yes_counted: number
  no_counted: number
  yes_percent_counted: number
  yes_predicted: number
  no_predicted: number
  yes_percent: number
  name: string
  is_final: boolean

  constructor(source: CantonResult) {
    this.id = source.geo_id
    this.yes_counted = source.yes_total - source.yes_predicted
    this.no_counted = source.no_total - source.no_predicted
    this.yes_predicted = source.yes_total
    this.no_predicted = source.no_total
    this.is_final = source.is_final
    this.yes_percent_counted =
      (this.yes_counted / (this.yes_counted + this.no_counted)) * 100
    this.yes_percent =
      (source.yes_total / (source.yes_total + source.no_total)) * 100
    this.name = source.name
  }
}
