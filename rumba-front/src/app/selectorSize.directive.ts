import { Directive, Input, ElementRef, OnInit, HostListener, ViewChild } from '@angular/core';
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
	@ViewChild('mySelector') selectorElem: ElementRef;

  constructor (private elementRef: ElementRef, private videoSrv: VideosServiceService ) {}

	ngOnInit(): void {
    // this.videoSrv.rangeValue
    //   .subscribe(
    //     (data: number) => {
		// 			console.log('currentWidth:::', data);
		// 			this.zoom = data;
    //     }
    //   );
		this.customMethod();
	}

	@HostListener('mousemove', ['$event'])
	onMouseMove(event: MouseEvent) {
		//console.log('moving', event);

	}

	@HostListener('dblclick', ['$event'])
	onMouseDoubleClick(event: MouseEvent) {
		console.log('double click', event);

		//this.elementRef.nativeElement.style.width += event.clientX + 'px';

	}

	@HostListener('mousedown', ['$event'])
	onMouseDown(event: MouseEvent) {
		console.log('mousedown', event);

	}

	@HostListener('mouseup', ['$event'])
	onMouseUp(event: MouseEvent) {
		console.log('mouseup', event);

	}

	resizer(offsetX: number) {
    // this.ownWidth += offsetX;
		// this.elementRef.nativeElement.style.width += (offsetX * 100) + 'px';
  }

	customMethod() {
		//Make the DIV element draggagle:
		//dragElement(document.getElementById("mySelector"));
		dragElement(this.elementRef.nativeElement)

		function dragElement(elmnt) {
		  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
		  elmnt.onmousedown = dragMouseDown;
			elmnt.ontouchstart = dragMouseDown;


			elmnt.ondblclick = elementWidth;



		  function dragMouseDown(e) {
		    e = e || window.event;
		    e.preventDefault();
		    // get the mouse cursor position at startup:
		    pos3 = e.clientX;
		    pos4 = e.clientY;
		    document.onmouseup = closeDragElement;
				document.ontouchend = closeDragElement;

				// call a function whenever the cursor moves:
		    document.onmousemove = elementDrag;
				document.ontouchmove = elementDrag;
			}

			function elementWidth(e) {
				e = e || window.event;
				e.preventDefault();

				elmnt.style.width = elmnt.style.width + e.clientX + 'px';

			}

		  function elementDrag(e) {
		    e = e || window.event;
		    e.preventDefault();
		    // calculate the new cursor position:
		    pos1 = pos3 - e.clientX;
		    pos2 = pos4 - e.clientY;
		    pos3 = e.clientX;
		    pos4 = e.clientY;
		    // set the element's new position:
		    //elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
		    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
		  }

		  function closeDragElement() {
		    /* stop moving when mouse button is released:*/
		    document.onmouseup = null;
		    document.onmousemove = null;

				//touch events
				document.ontouchend = null;
				document.ontouchmove = null;
		  }
		}
	}

}
