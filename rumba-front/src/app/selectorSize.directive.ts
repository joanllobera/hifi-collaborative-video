import { Directive, Input, ElementRef, OnInit, HostListener } from '@angular/core';
import { EditorService } from './editor.service';
import { VideosServiceService } from './videos-service.service';

@Directive({
	selector: '[appSelectorSize]'
})
export class SelectorSizeDirective implements OnInit {

	ownWidth: number;
	x: number = 100;
	oldX: number = 0;
	moving: boolean = false;
	zoom: number;

  constructor (private elementRef: ElementRef, private videoSrv: VideosServiceService ) {}

	ngOnInit(): void {
    this.videoSrv.rangeValue
      .subscribe(
        (data: number) => {
          //this.elementRef.nativeElement.style.width = data;
					console.log('currentWidth:::', data);
					this.zoom = data;
        }
      );
	}

	@HostListener('mousemove', ['$event'])
	onMouseMove(event: MouseEvent) {
		//console.log('moving', event);


		// if (!this.moving) {
		// 	return;
		// }
		// this.resizer(event.clientX - this.oldX);
		// this.oldX = event.clientX;
	}

	@HostListener('mousedown', ['$event'])
	onMouseDown(event: MouseEvent) {
		console.log('mousedown', event);

		this.elementRef.nativeElement.style.left = event.clientX + 'px';

		// this.moving = true;
		// this.oldX = event.clientX;
	}

	@HostListener('mouseup', ['$event'])
	onMouseUp(event: MouseEvent) {
		console.log('mouseup', event);
		//this.moving = false;
	}

	resizer(offsetX: number) {
    // this.ownWidth += offsetX;
		// this.elementRef.nativeElement.style.width += (offsetX * 100) + 'px';
  }

}
