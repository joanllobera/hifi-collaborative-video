import { Directive, ElementRef, ViewChild, HostListener, OnInit } from "@angular/core";

@Directive({
  selector: '[appClaudatorMove]'
})
export class ClaudatorMoveDirective implements OnInit {

  constructor(private elementRef: ElementRef) {}

  ngOnInit() {

  }

  @HostListener('click', ['$event'])
  onClick(event: MouseEvent) {

  }

  @HostListener('mousemove', ['$event'])
	onMouseMove(event: MouseEvent) {
		//console.log('moving', event);

	}

	@HostListener('touchstart', ['$event'])
	onTouchstart(event: MouseEvent) {
		//console.log('moving', event);
		alert('touchstart');

	}

	@HostListener('touchend', ['$event'])
	onTouchend(event: MouseEvent) {
		//console.log('moving', event);
		alert('touchend');

	}

	@HostListener('dblclick', ['$event'])
	onMouseDoubleClick(event: MouseEvent) {
		console.log('double click', event);

	}

	@HostListener('mousedown', ['$event'])
	onMouseDown(event: MouseEvent) {
		console.log('mousedown', event);
    this.elementRef.nativeElement.style.left = event.pageX + 'px';
	}

	@HostListener('mouseup', ['$event'])
	onMouseUp(event: MouseEvent) {
		console.log('mouseup', event);

	}


}
