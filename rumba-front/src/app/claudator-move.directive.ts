import { Directive, ElementRef, ViewChild, HostListener } from "@angular/core";

@Directive({
  selector: '[appClaudatorMove]'
})
export class ClaudatorMoveDirective {

  @ViewChild('claudator') clau: ElementRef;

  constructor(private elementRef: ElementRef) {}

  @HostListener('touchstart', ['$event'])
  onTouchstart (event: MouseEvent) {
    console.log('event::', event);
    console.log('element::', this.clau);
  }

}
