import { Directive, Input, ElementRef, OnInit } from '@angular/core';

@Directive({
  selector: '[appMargindelta]'
})
export class MargindeltaDirective implements OnInit {

  @Input() deltasize:number;
  thumbnailSize: number = 80; //size in pixels of the thumbnail in html view


  constructor(private elementRef: ElementRef) { }

  ngOnInit() {
    this.elementRef.nativeElement.style.marginLeft = (this.deltasize * this.thumbnailSize) + 'px';
  }

}
