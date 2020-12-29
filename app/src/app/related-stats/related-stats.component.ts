import {
  Component,
  Input,
  OnChanges,
  OnInit,
  SimpleChanges,
} from '@angular/core'
import { Observable } from 'rxjs'
import { BINARY_COLOR_SCHEME, COLOR_SCHEME } from '../settings'
import { RelatedResult } from '../votation'
import { VotationService } from '../votation.service'

interface Data {
  name: string
  percent: number
  series: [{ name: string; value: number }, { name: string; value: number }]
}

@Component({
  selector: 'app-related-stats',
  templateUrl: './related-stats.component.html',
  styleUrls: ['./related-stats.component.less'],
})
export class RelatedStatsComponent implements OnInit, OnChanges {
  @Input() votationId!: number
  @Input() cantonId?: number | null
  @Input() communeId?: number | null

  colorScheme = BINARY_COLOR_SCHEME

  result?: [Data][]

  constructor(private votationService: VotationService) {}

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    this.updateResults()
  }

  updateResults() {
    const newResults: [Data][] = []
    this.fetchRelatedResults().subscribe((results: RelatedResult[]) => {
      results.forEach((value: RelatedResult) => {
        newResults.push([
          {
            name: value.title,
            percent: (value.y / (value.y + value.n)) * 100,
            series: [
              { name: 'Ja', value: value.y },
              { name: 'Nein', value: value.n },
            ],
          },
        ])
      })
      this.result = newResults
    })
  }

  fetchRelatedResults(): Observable<RelatedResult[]> {
    if (this.communeId) {
      return this.votationService.getRelatedCommuneResults(
        this.votationId,
        this.communeId
      )
    } else if (this.cantonId) {
      return this.votationService.getRelatedCantonResults(
        this.votationId,
        this.cantonId
      )
    } else {
      return this.votationService.getRelatedResults(this.votationId)
    }
  }
}
