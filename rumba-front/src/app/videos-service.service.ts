import { Injectable } from '@angular/core';
import { Video } from './model/video.model';
import { Vimeo } from './model/vimeo.model';

import * as JSZip from 'jszip';
import { HttpClient } from '@angular/common/http';

import 'rxjs/Rx';  //needed for .map()

import { AppConfig } from './app-config';
import { Http, ResponseContentType } from '@angular/http';

@Injectable()
export class VideosServiceService {

  listOfVideos: Video[] = [
    new Video(0, 'Concert de Nadal', 'City Band', 'Auditori', new Vimeo('aaa', 'bbb')),
    new Video(1, 'Festes Mercé', 'Barcelona', 'Moll de la fusta', new Vimeo('aaa', 'bbb')),
    new Video(2, 'Primavera Sound', 'Slow Dive', 'Barcelona-Forum', new Vimeo('aaa', 'bbb')),
    new Video(3, 'Primavera Club', 'The Punsetes', 'Apolo', new Vimeo('aaa', 'bbb'))
  ];

  constructor(private httpClient: HttpClient, private http: Http) { }

  getVideos() {
    return this.listOfVideos.slice();
  }

  getThunmbnailsFromVideo() {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video/' + '5ad4b5fdc94b4c6bc260dd3c' + '/thumbs', {observe: 'body', responseType: 'blob'}).map(
        (response) => {
          console.log(response);
          return response;
        }
      );
  }



}
