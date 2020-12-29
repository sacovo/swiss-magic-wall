import { DatePipe, formatDate } from '@angular/common'
import {
  Component,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
} from '@angular/core'
import { COLOR_SCHEME, REFRESH_INTERVAL } from '../settings'
import { VotationDataSeries } from '../votation'
import { VotationService } from '../votation.service'

@Component({
  selector: 'app-votation-stats',
  templateUrl: './votation-stats.component.html',
  styleUrls: ['./votation-stats.component.less'],
})
export class VotationStatsComponent implements OnInit, OnDestroy, OnChanges {
  data: VotationDataSeries[] = []
  xTicks: Date[] = []
  @Input() votationId!: number
  @Input() cantonId: number | null = null
  @Input() communeId: number | null = null
  interval: number | undefined

  colorScheme = COLOR_SCHEME

  view: [number, number] = [580, 180]
  legend: boolean = true
  showLabels: boolean = true
  animations: boolean = false
  xAxis: boolean = true
  yAxis: boolean = true
  showYAxisLabel: boolean = true
  showXAxisLabel: boolean = true
  xAxisLabel: string = 'Zeit'
  yAxisLabel: string = 'Zustimmung in %'
  timeline: boolean = false

  xAxisTickFormatting = (t: Date) => formatDate(t, 'HH:mm:ss', 'de-CH')

  constructor(private votationService: VotationService) {}

  ngOnInit(): void {
    this.interval = window.setInterval(() => {
      this.updateResults()
    }, REFRESH_INTERVAL)

    this.updateResults()
  }

  ngOnChanges(changes: SimpleChanges): void {
    if ('cantonId' in changes || 'communeId' in changes) {
      this.updateResults()
    }
  }

  updateResults() {
    if (this.communeId) {
      this.votationService
        .getVotationStatsCommune(this.votationId, this.communeId)
        .subscribe((result: VotationDataSeries[]) => {
          this.data = result
          this.updateXTicks()
        })
    } else if (this.cantonId) {
      this.votationService
        .getVotationStats(this.votationId, this.cantonId)
        .subscribe((result: VotationDataSeries[]) => {
          this.data = result
          this.updateXTicks()
        })
    } else {
      this.votationService
        .getVotationStats(this.votationId)
        .subscribe((result: VotationDataSeries[]) => {
          this.data = result
          this.updateXTicks()
        })
    }
  }

  ngOnDestroy(): void {
    window.clearInterval(this.interval)
  }

  updateXTicks(): void {
    const entries = this.data[0].series
    const stepSize = Math.max(Math.round(entries.length / 8), 1)
    const steps = []
    for (let i = 0; i < entries.length; i += stepSize) {
      steps.push(entries[Math.round(i)].name)
    }
    this.xTicks = steps
  }
}
