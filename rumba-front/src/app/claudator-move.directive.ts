import { Directive, ElementRef, ViewChild, HostListener, OnInit } from "@angular/core";

@Directive({
  selector: '[appClaudatorMove]'
})
export class ClaudatorMoveDirective implements OnInit {

  constructor(private elementRef: ElementRef) {}

  ngOnInit() {

  }

  @HostListener('touchstart', ['$event'])
  onTouchstart (event: MouseEvent) {

  }

  @HostListener('mousedown', ['$event'])
  onMouseDown(event: MouseEvent) {

  }

  @HostListener('click', ['$event'])
  onClick(event: MouseEvent) {
    this.elementRef.nativeElement.style.left = event.pageX + 'px';
  }



}
