import { ComponentFixture, TestBed } from '@angular/core/testing'

import { VotationDatesComponent } from './votation-dates.component'

describe('VotationDatesComponent', () => {
  let component: VotationDatesComponent
  let fixture: ComponentFixture<VotationDatesComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VotationDatesComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(VotationDatesComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
