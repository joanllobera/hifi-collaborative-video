export class Session {

  public concert: string;
  public band: string;
  public date: number;
  public is_public: boolean;
  public location: string;

  constructor (concert: string, band: string, date: number, is_public: boolean, location: string) {
    
    this.concert = concert;
    this.band = band;
    this.date = date;
    this.is_public = is_public;
    this.location = location;

  }

}
