import { Component, OnInit } from '@angular/core'
import { Title } from '@angular/platform-browser'
import { ActivatedRoute, Router } from '@angular/router'
import { REFRESH_INTERVAL } from '../settings'
import { TopoService } from '../topo.service'
import { getTitle, Votation } from '../votation'
import { VotationService } from '../votation.service'
import { CantonEntry, CommuneEntry } from './results'

@Component({
  selector: 'app-votation-table',
  templateUrl: './votation-table.component.html',
  styleUrls: ['./votation-table.component.less'],
})
export class VotationTableComponent implements OnInit {
  votation!: Votation
  canton_rows: CantonEntry[] = []
  commune_rows: CommuneEntry[] = []
  loading: boolean = false

  interval: number | undefined
  constructor(
    private votationService: VotationService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title,
    private topoService: TopoService
  ) {}

  ngOnInit(): void {
    const votationId = this.route.snapshot.paramMap.get('id')
    this.topoService.getTopoData()
    if (votationId) {
      this.votationService.getVotation(votationId).subscribe((votation) => {
        this.updateVotation(votation)
        this.titleService.setTitle(
          getTitle(this.votation, 'de') + ' - Magic Wall'
        )
      })
      this.interval = window.setInterval(() => {
        this.reloadVotation()
      }, REFRESH_INTERVAL)
    }
  }

  reloadVotation(): void {
    if (this.votation) {
      this.loading = true
      this.votationService
        .getVotation(this.votation.id)
        .subscribe((votation) => {
          this.loading = false
          this.updateVotation(votation)
          if (votation.is_finished) {
            clearInterval(this.interval)
          }
        })
    }
  }

  updateVotation(votation: Votation): void {
    this.votation = votation
    this.canton_rows = votation.cantons.map((result) => new CantonEntry(result))
    this.commune_rows = votation.communes.map(
      (result) => new CommuneEntry(result, this.topoService)
    )
  }

  getTitle(): string {
    return getTitle(this.votation, 'de')
  }
}
