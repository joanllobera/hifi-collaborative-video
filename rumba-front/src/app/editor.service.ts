import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class EditorService {

  currentWidth = new Subject<number>();

  constructor(private editorSrv: EditorService) { }

}
