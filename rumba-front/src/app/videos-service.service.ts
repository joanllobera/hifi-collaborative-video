import { Injectable } from '@angular/core';
import { Video } from './model/video.model';
import { Vimeo } from './model/vimeo.model';

@Injectable()
export class VideosServiceService {

  listOfVideos: Video[] = [
    new Video(0, 'Concert de Nadal', 'City Band', 'Auditori', new Vimeo('aaa', 'bbb')),
    new Video(1, 'Festes Mercé', 'Barcelona', 'Moll de la fusta', new Vimeo('aaa', 'bbb')),
    new Video(2, 'Primavera Sound', 'Slow Dive', 'Barcelona-Forum', new Vimeo('aaa', 'bbb')),
    new Video(3, 'Primavera Club', 'The Punsetes', 'Apolo', new Vimeo('aaa', 'bbb'))
  ];

  constructor() { }

  getVideos() {
    return this.listOfVideos.slice();
  }

}
