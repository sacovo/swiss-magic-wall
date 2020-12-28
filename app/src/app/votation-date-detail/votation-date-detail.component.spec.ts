import { ComponentFixture, TestBed } from '@angular/core/testing'

import { VotationDateDetailComponent } from './votation-date-detail.component'

describe('VotationDateDetailComponent', () => {
  let component: VotationDateDetailComponent
  let fixture: ComponentFixture<VotationDateDetailComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VotationDateDetailComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(VotationDateDetailComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
