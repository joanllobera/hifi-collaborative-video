import { Injectable } from "@angular/core";
import { Http , Response, ResponseContentType } from "@angular/http";
import { HttpClient } from '@angular/common/http';

import 'rxjs/Rx';  //needed for .map()

import { AppConfig } from '../app-config';

@Injectable()
export class SessionService {

  url: string;

  constructor(private http: Http, private httpClient: HttpClient) {}

  startSession(session: any) {
    this.url = AppConfig.START_SESSON;
    return this.http.post(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/', session);
  }

  closeSession (id: string) {
    return this.http.put(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + id + '/stop', {});
  }

  getSessionById (id: string) {
    return this.http.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + id);
  }
  getSession () {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/active' );
  }

  uploadLogo (id: string, selectedFile: File) {
    const fd = new FormData();
    fd.append('image', selectedFile, selectedFile.name);
    return this.httpClient.post(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + id + '/logo', fd);
  }

  getLogoById (id: string) {
    // return this.http.get(AppConfig.API_ENDPOINT + '/sessions/' + id + '/logo')
    //   .map(
    //     (response: Response) => {
    //       return response;
    //     }
    //   );
    return this.http.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + id + '/logo', { responseType: ResponseContentType.Blob });
  }

  getAudioStatus () {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/audio/microphone/state');
  }



}
