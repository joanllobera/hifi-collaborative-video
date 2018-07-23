import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import 'rxjs/Rx';

import { AppConfig } from './app-config';

@Injectable()
export class RecordService {

  constructor(private httpClient: HttpClient) { }

  startRecordingVideo() {
    return this.httpClient.post(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video/', {});
  }

  stopRecordingVideo(videoId: string) {
    return this.httpClient.put(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video/' + videoId + '/stop', {});
  }

  initializeRumbaSession(session_id: string) {
    return this.httpClient.put(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + session_id, {});
  }

}
