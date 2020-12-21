import { TestBed } from '@angular/core/testing';

import { VotationDateService } from './votation-date.service';

describe('VotationDateService', () => {
  let service: VotationDateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VotationDateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
