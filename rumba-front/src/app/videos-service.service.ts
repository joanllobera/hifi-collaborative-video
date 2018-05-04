import { Injectable } from '@angular/core';
import { Video } from './model/video.model';
import { Vimeo } from './model/vimeo.model';

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

  getThunmbnailsFromVideo(id:string) {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video/' + id + '/thumbs', {observe: 'body', responseType: 'blob'}).map(
        (response) => {
          return response;
        }
      );
  }

  getAllVideos() {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/sessions/' + '5ad09d5ec94b4c7adb5dbe27' + '/videos/all', {observe: 'body', responseType: 'json'});
  }

  buildVideo(json) {
    return this.httpClient.post(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/edition/' + '5adef60dc94b4c5642d28cf3' + '/build', json, {observe: 'body', responseType: 'blob'});

    // return this.http.post(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/edition/' + '5adef60dc94b4c5642d28cf3' + '/build', json, { responseType: ResponseContentType.Blob });
  }

  getRecordedVideos() {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video', {observe: 'body', responseType: 'json'});
  }

  getVideoFirstThumbnail(videoId: string) {
    return this.httpClient.get(AppConfig.API_ENDPOINT + AppConfig.API_VERSION + '/video/' + videoId + '/first_thumb', {observe: 'body', responseType: 'json'});
  }



}
