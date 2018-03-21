export class Video {

  public id: number;
  public name: string;
  public band: string;
  public local: string;
  public vimeo_user: string;
  public vimeo_pwd: string;

  constructor (id: number, name: string, band: string, local: string, vimeo_user: string, vimeo_pwd: string) {
    this.id = id;
    this.name = name;
    this.band = band;
    this.local = local;
    this.vimeo_user = vimeo_user;
    this.vimeo_pwd = vimeo_pwd;
  }
  

}
