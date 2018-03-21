import { Injectable } from '@angular/core';
import { Video } from './model/video.model';

@Injectable()
export class VideosServiceService {

  listOfVideos: Video[] = [
    new Video(0, 'Concert de Nadal', 'Corbera Band', 'Auditori', 'enric', '111'),
    new Video(1, 'Festes Mercé', 'Barcelona', 'Moll de la fusta', 'enric', '111'),
    new Video(2, 'Primavera Sound', 'Slow Dive', 'Barcelona-Forum', 'enric', '111'),
    new Video(3, 'Primavera Club', 'The Punsetes', 'Apolo', 'enric', '111')
  ];

  constructor() { }

  getVideos() {
    return this.listOfVideos.slice();
  }

}
