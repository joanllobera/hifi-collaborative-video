import { Directive, Input, ElementRef, OnInit } from '@angular/core';

@Directive({
	selector: '[appSelectorSize]'
})
export class SelectorSizeDirective implements OnInit {

  constructor (private elementRef: ElementRef) {}

	ngOnInit(): void {
    this.elementRef.nativeElement.style.width;
	}

  onClickSeparator($event) {
    console.log($event);
  }


}
