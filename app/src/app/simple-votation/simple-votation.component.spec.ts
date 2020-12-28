import { ComponentFixture, TestBed } from '@angular/core/testing'

import { SimpleVotationComponent } from './simple-votation.component'

describe('SimpleVotationComponent', () => {
  let component: SimpleVotationComponent
  let fixture: ComponentFixture<SimpleVotationComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SimpleVotationComponent],
    }).compileComponents()
  })

  beforeEach(() => {
    fixture = TestBed.createComponent(SimpleVotationComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
