import { Component, OnInit } from '@angular/core'
import { Title } from '@angular/platform-browser'
import { ActivatedRoute, Router } from '@angular/router'
import { TopoService } from '../topo.service'
import { getTitle, Votation } from '../votation'
import { VotationService } from '../votation.service'

@Component({
  selector: 'app-votation-table',
  templateUrl: './votation-table.component.html',
  styleUrls: ['./votation-table.component.less'],
})
export class VotationTableComponent implements OnInit {
  votation!: Votation
  interval: number | undefined
  constructor(
    private votationService: VotationService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title,
    private topoService: TopoService
  ) {}


  getNameFor(id: number): string {
    return this.topoService.getNameFor(id);
  }

  ngOnInit(): void {
    const votationId = this.route.snapshot.paramMap.get('id')
    this.topoService.getTopoData();
    if (votationId) {
      this.votationService.getVotation(votationId).subscribe((votation) => {
        this.votation = votation
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
          this.votation = votation
          if (votation.is_finished) {
            clearInterval(this.interval)
          }
        })
    }
  }

  getTitle(): string {
    return getTitle(this.votation, 'de')
  }
}
