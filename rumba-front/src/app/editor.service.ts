import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class EditorService {



  newZoomValue = new Subject<number>();
  currentWidth = new Subject<number>();

  constructor() { }

}
