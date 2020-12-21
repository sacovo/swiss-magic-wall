import { ApplicationRef, Component, OnInit, ViewChild } from '@angular/core'
import { Title } from '@angular/platform-browser'
import { Router, ActivatedRoute } from '@angular/router'
import { MapComponent } from '../map/map.component'
import { Votation, getTitle, CantonResult } from '../votation'
import { VotationService } from '../votation.service'

@Component({
  selector: 'app-votation-detail',
  templateUrl: './votation-detail.component.html',
  styleUrls: ['./votation-detail.component.less'],
})
export class VotationDetailComponent implements OnInit {
  votation!: Votation
  interval: number | undefined

  selectedCantonId: number | null = null
  selectedCantonName: string = ''
  selectedCommuneId: number | null = null
  selectedCommuneName: string = ''
  index: any = {};
  cantonCounted: boolean = false
  communeCounted: boolean = false

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA'],
  }

  results: any[] = []

  cantonResults: any[] = []
  communeResults: any[] = []

  @ViewChild(MapComponent) map!: MapComponent

  constructor(
    private votationService: VotationService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {}

  buildIndex() {

    for(let i = 0; i < this.votation.communes.length; i++) {
      this.index[`${this.votation.communes[i].geo_id}`] = i;
    }
  }

  ngOnInit(): void {
    const votationId = this.route.snapshot.paramMap.get('id')
    if (votationId) {
      this.votationService.getVotation(votationId).subscribe((votation) => {
        this.votation = votation
        this.updateResults();
        this.buildIndex();
        this.map.updateCantons(votation.cantons)
        this.map.updateCommunes(votation.communes)
        this.titleService.setTitle(
          getTitle(this.votation, 'de') + ' - Magic Wall'
        )
      })
      this.interval = window.setInterval(() => {
        this.reloadVotation()
      }, 2000)
    }
  }

  reloadVotation(): void {
    if (this.votation) {
      this.votationService
        .getVotation(this.votation.id)
        .subscribe((votation) => {
          Object.assign(this.votation, votation)
          this.updateResults();
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
        {name: "Gezählt", series: [
          {name: "JA", value: this.votation.yes_counted },
          {name: "NEIN", value:  this.votation.no_counted },
        ]},
        {name: "Prognose", series: [
          {name: "JA", value: this.votation.yes_counted + this.votation.yes_predicted},
          {name: "NEIN", value: this.votation.no_counted + this.votation.no_predicted},
        ]},
      ]

      this.updateCantonalResults();
      this.updateCommuneResults();
    }
  }

  updateCantonalResults() {
    if(this.votation && this.selectedCantonId){
      const result = this.votation.cantons.find((result) => result.geo_id == this.selectedCantonId)
      if (result) {
        this.cantonResults = [
          {name: "Gezählt", series: [
            {name: "JA", value: result.yes_total - result.yes_predicted},
            {name: "NEIN", value:  result.no_total - result.no_predicted },
          ]},
          {name: "Prognose", series: [
            {name: "JA", value: result.yes_total},
            {name: "NEIN", value: result.no_total},
          ]},
        ]
        this.cantonCounted = result.is_final;
      }

    }
  }


  updateCommuneResults() {
    if(this.votation && this.selectedCommuneId){
      const index = this.index[`${this.selectedCommuneId}`];
      if (index >= 0) {
        const result = this.votation.communes[index]
        this.communeResults = [
          {name: "Nein", value: result.no_total},
          {name: "Ja", value: result.yes_total},
        ]
        this.communeCounted = result.is_final;
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
    this.selectCommune(+event.properties.id, event.properties.name)
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
    this.updateCantonalResults();
  }

  selectCommune(id: number, name: string) {
    this.selectedCommuneId = id
    this.selectedCommuneName = name
    this.updateCommuneResults();
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
}
