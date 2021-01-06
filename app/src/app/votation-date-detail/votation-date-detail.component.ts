import { formatDate } from '@angular/common'
import {
  Component,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
} from '@angular/core'
import { Title } from '@angular/platform-browser'
import { REFRESH_INTERVAL } from '../settings'
import { VotationDate } from '../votation'
import { VotationDateService } from '../votation-date.service'

@Component({
  selector: 'app-votation-date-detail',
  templateUrl: './votation-date-detail.component.html',
  styleUrls: ['./votation-date-detail.component.less'],
})
export class VotationDateDetailComponent
  implements OnInit, OnDestroy, OnChanges {
  @Input() dateId!: number

  date?: VotationDate
  interval: number | undefined

  constructor(private dateService: VotationDateService, private title: Title) {}

  ngOnInit(): void {
    this.getVotationDate()
  }

  getVotationDate() {
    if (this.dateId > 0) {
      this.date = undefined
      this.dateService
        .getVotationDate(this.dateId)
        .subscribe((date: VotationDate) => {
          this.date = date

          this.title.setTitle(
            formatDate(date.start_date, 'longDate', 'de-CH') +
              ' - Swiss Election Map'
          )

          if (this.interval) {
            window.clearInterval(this.interval)
          }

          this.interval = window.setInterval(() => {
            this.updateVotationDates()
          }, REFRESH_INTERVAL)
        })
    }
  }

  ngOnDestroy(): void {
    if (this.interval) {
      window.clearInterval(this.interval)
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.dateId) {
      this.getVotationDate()
    }
  }

  updateVotationDates(): void {
    if (this.date && !this.date.is_finished) {
      this.dateService.getVotationDate(this.date.id).subscribe((newDate) => {
        this.date = newDate
        if (newDate.is_finished) {
          window.clearInterval(this.interval)
          this.interval = undefined
        }
      })
    }
  }
}
