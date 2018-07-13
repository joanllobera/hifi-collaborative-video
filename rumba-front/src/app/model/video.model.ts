import { Vimeo } from './vimeo.model';

export class Video {

  public id: number;
  public name: string;
  public band: string;
  public local: string;
  public vimeo: Vimeo;

  constructor (id: number, name: string, band: string, local: string, vimeo: Vimeo) {
    this.id = id;
    this.name = name;
    this.band = band;
    this.local = local;
    this.vimeo = vimeo;
  }


}
