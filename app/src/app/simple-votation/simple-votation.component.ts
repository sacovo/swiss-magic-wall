import { Component, Input, OnInit, SimpleChanges } from '@angular/core'
import { SimpleVotation, getTitle } from '../votation'

import { COLOR_SCHEME, BINARY_COLOR_SCHEME } from '../settings'

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

  colorScheme = COLOR_SCHEME
  binaryColorScheme = BINARY_COLOR_SCHEME

  constructor() {}

  title(): string {
    return getTitle(this.votation, this.language_code)
  }

  updateResults(): void {
    this.results = [
      { name: 'Ja gezählt', value: this.votation.yes_counted },
      { name: 'Ja prognostiziert', value: this.votation.yes_predicted },
      { name: 'Nein prognostiziert', value: this.votation.no_predicted },
      { name: 'Nein gezählt', value: this.votation.no_counted },
    ]

    this.prediction = [
      {
        name: 'Ja',
        value: this.votation.yes_counted + this.votation.yes_predicted,
      },
      {
        name: 'Nein',
        value: this.votation.no_counted + this.votation.no_predicted,
      },
    ]

    this.counted = [
      { name: 'Ja', value: this.votation.yes_counted },
      { name: 'Nein', value: this.votation.no_counted },
    ]
  }

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes) {
      this.updateResults()
    }
  }
}
