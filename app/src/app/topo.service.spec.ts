import { TestBed } from '@angular/core/testing';

import { TopoService } from './topo.service';

describe('TopoService', () => {
  let service: TopoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TopoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
