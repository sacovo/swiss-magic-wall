import { Component, Input, OnInit, SimpleChanges } from '@angular/core'
import { SimpleVotation, getTitle } from '../votation'

@Component({
  selector: 'app-simple-votation',
  templateUrl: './simple-votation.component.html',
  styleUrls: ['./simple-votation.component.less'],
})
export class SimpleVotationComponent implements OnInit {
  readonly language_code = 'de'

  @Input() votation!: SimpleVotation

  results: any[] = []
  prediction: any[] = []
  counted: any[] = []
  view: [number, number] = [700, 400]

  // options
  gradient: boolean = false
  showLegend: boolean = false

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA'],
  }

  binaryColorScheme = {
    domain: ['#00ff00', '#ff0000'],
  }

  constructor() {}

  title(): string {
    return getTitle(this.votation, this.language_code)
  }

  updateResults(): void {
    this.results = [
      { name: 'Nein gezählt', value: this.votation.no_counted },
      { name: 'Ja gezählt', value: this.votation.yes_counted },
      { name: 'Nein prognostiziert', value: this.votation.no_predicted },
      { name: 'Ja prognostiziert', value: this.votation.yes_predicted },
    ]

    this.prediction = [
      {
        name: 'Nein',
        value: this.votation.no_counted + this.votation.no_predicted,
      },
      {
        name: 'Ja',
        value: this.votation.yes_counted + this.votation.yes_predicted,
      },
    ]

    this.counted = [
      { name: 'Nein', value: this.votation.no_counted },
      { name: 'Ja', value: this.votation.yes_counted },
    ]
  }

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes) {
      this.updateResults()
    }
  }
}
