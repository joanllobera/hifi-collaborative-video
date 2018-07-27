import { Directive, Input, ElementRef, OnInit } from '@angular/core';
import { EditorService } from './editor.service';

@Directive({
	selector: '[appSelectorSize]'
})
export class SelectorSizeDirective implements OnInit {

  constructor (private elementRef: ElementRef, private editorSrv: EditorService) {}

	ngOnInit(): void {
    this.editorSrv.currentWidth
      .subscribe(
        (data) => {
          this.elementRef.nativeElement.style.width = data;
					alert(data);
        }
      );


	}



}
