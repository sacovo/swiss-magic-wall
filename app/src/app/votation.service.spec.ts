import { TestBed } from '@angular/core/testing';

import { VotationService } from './votation.service';

describe('VotationService', () => {
  let service: VotationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VotationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
