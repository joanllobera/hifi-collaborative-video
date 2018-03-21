import { TestBed, inject } from '@angular/core/testing';

import { VideosServiceService } from './videos-service.service';

describe('VideosServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VideosServiceService]
    });
  });

  it('should be created', inject([VideosServiceService], (service: VideosServiceService) => {
    expect(service).toBeTruthy();
  }));
});
