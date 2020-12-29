import { TestBed } from '@angular/core/testing';

import { RelatedResultsService } from './related-results.service';

describe('RelatedResultsService', () => {
  let service: RelatedResultsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RelatedResultsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
