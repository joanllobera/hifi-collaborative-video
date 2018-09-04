import { Directive, ElementRef, ViewChild, HostListener, OnInit } from "@angular/core";

@Directive({
  selector: '[appClaudatorMove]'
})
export class ClaudatorMoveDirective implements OnInit {

  @ViewChild('claudator') clau: ElementRef;

  constructor(private elementRef: ElementRef) {}

  ngOnInit() {
    //this.moveSelector();
  }

  @HostListener('touchstart', ['$event'])
  onTouchstart (event: MouseEvent) {
    console.log('event::', event);
    console.log('element::', this.clau);
    console.log('this.elementRef::', this.elementRef);
  }

  @HostListener('mousedown', ['$event'])
  onMouseDown(event: MouseEvent) {
    console.log(this.elementRef);
  }

  moveSelector() {
		//Make the DIV element draggagle:
		//dragElement(document.getElementById("mySelector"));
		dragElement(this.elementRef.nativeElement)

		function dragElement(elmnt) {
		  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
		  elmnt.onmousedown = dragMouseDown;
			elmnt.ontouchstart = dragMouseDown;

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
