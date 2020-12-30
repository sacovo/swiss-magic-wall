import { ComponentFixture, TestBed } from '@angular/core/testing'

import { RelatedStatsComponent } from './related-stats.component'

describe('RelatedStatsComponent', () => {
  let component: RelatedStatsComponent
  let fixture: ComponentFixture<RelatedStatsComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RelatedStatsComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(RelatedStatsComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
