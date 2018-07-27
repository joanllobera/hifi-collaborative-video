import { Directive, Input, ElementRef, OnInit, HostListener } from '@angular/core';
import { EditorService } from './editor.service';

@Directive({
	selector: '[appSelectorSize]'
})
export class SelectorSizeDirective implements OnInit {

	y: number = 100;
	oldY: number = 0;
	moving: boolean = false;

  constructor (private elementRef: ElementRef, private editorSrv: EditorService) {}

	ngOnInit(): void {
    this.editorSrv.currentWidth
      .subscribe(
        (data) => {
          //this.elementRef.nativeElement.style.width = data;
        }
      );
	}

	@HostListener('kkk1:mousemove', ['$event'])
	onMouseMove(event: MouseEvent) {
		console.log('moving', event);
	}


}
