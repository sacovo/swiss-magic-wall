import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core'
import { Title } from '@angular/platform-browser'
import { Router, ActivatedRoute } from '@angular/router'
import { MapComponent } from '../map/map.component'
import { Votation, getTitle, CantonResult } from '../votation'
import { VotationService } from '../votation.service'

import {
  COLOR_SCHEME,
  BINARY_COLOR_SCHEME,
  REFRESH_INTERVAL,
} from '../settings'

@Component({
  selector: 'app-votation-detail',
  templateUrl: './votation-detail.component.html',
  styleUrls: ['./votation-detail.component.less'],
})
export class VotationDetailComponent implements OnInit, OnDestroy {
  votation!: Votation
  interval: number | undefined

  selectedCanton: CantonResult | undefined

  colorScheme = COLOR_SCHEME
  binaryColorScheme = BINARY_COLOR_SCHEME

  selectedCantonId: number | null = null
  selectedCantonName: string = ''
  selectedCommuneId: number | null = null
  selectedCommuneName: string = ''
  index: any = {}
  cantonCounted: boolean = false
  communeCounted: boolean = false

  loading: boolean = true

  results: any[] = []

  cantonResults: any[] = []
  pieResults: any[] = []
  pieResultsCanton: any[] = []
  communeResults: any[] | undefined = []

  @ViewChild(MapComponent) map!: MapComponent

  constructor(
    private votationService: VotationService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {}

  buildIndex() {
    for (let i = 0; i < this.votation.communes.length; i++) {
      this.index[`${this.votation.communes[i].geo_id}`] = i
    }
  }

  ngOnInit(): void {
    const votationId = this.route.snapshot.paramMap.get('id')
    if (votationId) {
      this.votationService.getVotation(votationId).subscribe((votation) => {
        this.votation = votation
        this.loading = false
        this.updateResults()
        this.buildIndex()
        this.map.updateCantons(votation.cantons)
        this.map.updateCommunes(votation.communes)
        this.titleService.setTitle(
          getTitle(this.votation, 'de') + ' - Magic Wall'
        )
      })
      this.interval = window.setInterval(() => {
        this.reloadVotation()
      }, REFRESH_INTERVAL)
    }
  }

  ngOnDestroy(): void {
    if (this.interval) {
      clearInterval(this.interval)
    }
  }

  reloadVotation(): void {
    if (this.votation) {
      this.votationService
        .getVotation(this.votation.id)
        .subscribe((votation) => {
          Object.assign(this.votation, votation)
          this.updateResults()
          this.redrawMap()
          if (votation.is_finished) {
            clearInterval(this.interval)
          }
        })
    }
  }

  updateResults() {
    if (this.votation) {
      this.results = [
        {
          name: 'Gezählt',
          series: [
            { name: 'JA', value: this.votation.yes_counted },
            { name: 'NEIN', value: this.votation.no_counted },
          ],
        },
        {
          name: 'Prognose',
          series: [
            {
              name: 'JA',
              value: this.votation.yes_counted + this.votation.yes_predicted,
            },
            {
              name: 'NEIN',
              value: this.votation.no_counted + this.votation.no_predicted,
            },
          ],
        },
      ]

      this.pieResults = [
        { name: 'Ja gezählt', value: this.votation.yes_counted },
        { name: 'Ja prognostiziert', value: this.votation.yes_predicted },
        { name: 'Nein prognostiziert', value: this.votation.no_predicted },
        { name: 'Nein gezählt', value: this.votation.no_counted },
      ]

      this.updateCantonalResults()
      this.updateCommuneResults()
    }
  }

  async updateCantonalResults() {
    if (this.votation && this.selectedCantonId) {
      this.selectedCanton = this.getSelectCantonResult()
      const result = this.selectedCanton
      if (result) {
        this.cantonResults = [
          {
            name: 'Gezählt',
            series: [
              { name: 'JA', value: result.yes_total - result.yes_predicted },
              { name: 'NEIN', value: result.no_total - result.no_predicted },
            ],
          },
          {
            name: 'Prognose',
            series: [
              { name: 'JA', value: result.yes_total },
              { name: 'NEIN', value: result.no_total },
            ],
          },
        ]
        this.pieResultsCanton = [
          {
            name: 'JA gezählt',
            value: result.yes_total - result.yes_predicted,
          },
          { name: 'JA prognostiziert', value: result.yes_predicted },
          { name: 'NEIN prognostiziert', value: result.no_predicted },
          {
            name: 'NEIN gezählt',
            value: result.no_total - result.no_predicted,
          },
        ]
        this.cantonCounted = result.is_final
      }
    }
  }

  updateCommuneResults() {
    if (this.votation && this.selectedCommuneId) {
      const index = this.index[`${this.selectedCommuneId}`]
      if (index && index >= 0) {
        const result = this.votation.communes[index]
        this.communeResults = [
          { name: 'Ja', value: result.yes_total },
          { name: 'Nein', value: result.no_total },
        ]
        this.communeCounted = result.is_final
      } else {
        this.communeResults = undefined
        this.communeCounted = false
      }
    }
  }

  cantonEvent(event: any): void {
    this.deselectCanton()
    if (event) {
      this.selectCanton(+event.properties.id, event.properties.name)
    }
  }

  communeEvent(event: any): void {
    this.selectCommune(+event.properties.vogenr, event.properties.vogename)
  }

  redrawMap(event?: any): void {
    if (this.votation) {
      this.map.updateCantons(this.votation.cantons)
      this.map.updateCommunes(this.votation.communes)
    }
  }

  selectCanton(id: number, name: string) {
    this.selectedCantonId = id
    this.selectedCantonName = name
    this.selectedCanton = this.getSelectCantonResult()
    this.updateCantonalResults()
  }

  selectCommune(id: number, name: string) {
    this.selectedCommuneId = id
    this.selectedCommuneName = name
    this.updateCommuneResults()
  }

  deselectCanton() {
    this.selectedCantonId = null
    this.selectedCantonName = ''
    this.deselectCommune()
  }

  deselectCommune() {
    this.selectedCommuneId = null
    this.selectedCommuneName = ''
  }

  getSelectCantonResult(): CantonResult | undefined {
    const result = this.votation?.cantons.find(
      (canton) => canton.geo_id === (this.selectedCantonId as number)
    )

    return result
  }

  goToVotation(id: number) {
    this.router.navigate(['/votation', { id: id }])
  }

  getTitle(): string {
    if (this.votation) {
      return getTitle(this.votation, 'de')
    }

    return ''
  }

  yesCountedPercent(): number {
    return (
      (this.votation.yes_counted /
        (this.votation.yes_counted + this.votation.no_counted)) *
      100
    )
  }

  yesPredictedPercent(): number {
    return (
      ((this.votation.yes_predicted + this.votation.yes_counted) /
        (this.votation.yes_predicted +
          this.votation.no_predicted +
          this.votation.yes_counted +
          this.votation.no_counted)) *
      100
    )
  }

  yesCountedPercentCanton(): number {
    if (this.selectedCanton) {
      return (
        ((this.selectedCanton.yes_total - this.selectedCanton.yes_predicted) /
          (this.selectedCanton.yes_total -
            this.selectedCanton.yes_predicted +
            this.selectedCanton.no_total -
            this.selectedCanton.no_predicted)) *
        100
      )
    }
    return 0
  }

  yesPredictedPercentCanton(): number {
    if (this.selectedCanton) {
      return (
        (this.selectedCanton.yes_total /
          (this.selectedCanton.yes_total + this.selectedCanton.no_total)) *
        100
      )
    }
    return 0
  }

  yesPercentCommune(): number {
    return this.communeResults
      ? (this.communeResults[0]['value'] /
          (this.communeResults[1]['value'] + this.communeResults[0]['value'])) *
          100
      : 0
  }
}
