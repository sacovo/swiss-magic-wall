import { Component, OnInit, ViewChild } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { VotationDate } from '../votation'
import {VotationDateDetailComponent} from '../votation-date-detail/votation-date-detail.component'
import { VotationDateService } from '../votation-date.service'

@Component({
  selector: 'app-votation-dates',
  templateUrl: './votation-dates.component.html',
  styleUrls: ['./votation-dates.component.less'],
})
export class VotationDatesComponent implements OnInit {
  votationDates: VotationDate[] = []
  selectedDate: number = 0

  @ViewChild(VotationDateDetailComponent) dateDetail!: VotationDateDetailComponent

  constructor(
    private votationDateService: VotationDateService,
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
    this.fetchVotationDates()
  }

  fetchVotationDates(): void {
    this.votationDateService.getVotationDates().subscribe((votationDates) => {
      this.votationDates = votationDates
      const id = this.route.snapshot.paramMap.get('id');
      console.log(id);
      if (id) {
        this.selectDate(+id);
      } else {
        this.selectDate(this.votationDates[0].id)
      }
    })
  }

  selectDate(id: number): void {
    this.selectedDate = id
  }
}
