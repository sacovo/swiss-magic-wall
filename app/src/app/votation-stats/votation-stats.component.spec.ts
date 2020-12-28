import { ComponentFixture, TestBed } from '@angular/core/testing'

import { VotationStatsComponent } from './votation-stats.component'

describe('VotationStatsComponent', () => {
  let component: VotationStatsComponent
  let fixture: ComponentFixture<VotationStatsComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VotationStatsComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(VotationStatsComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
