import { ComponentFixture, TestBed } from '@angular/core/testing'

import { VotationTableComponent } from './votation-table.component'

describe('VotationTableComponent', () => {
  let component: VotationTableComponent
  let fixture: ComponentFixture<VotationTableComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VotationTableComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(VotationTableComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
