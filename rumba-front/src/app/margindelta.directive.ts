import { Directive, Input, ElementRef, OnInit } from '@angular/core';
import { VideosServiceService } from './videos-service.service';

@Directive({
  selector: '[appMargindelta]'
})
export class MargindeltaDirective implements OnInit {

  @Input() deltasize:number;
  thumbnailSize: number; //size in pixels of the thumbnail in html view


  constructor(private elementRef: ElementRef, private videoSrv: VideosServiceService) { }

  ngOnInit() {

    let width = window.innerWidth ||
                document.documentElement.clientWidth ||
                document.body.clientWidth;

    this.elementRef.nativeElement.style.marginLeft = (this.deltasize * (8 * 10)) + 'px';
    this.elementRef.nativeElement.style.minWidth = 1000 + "px";

    this.videoSrv.rangeValue
      .subscribe(
        (zoomLevel: number) => {
          this.thumbnailSize = 8 * zoomLevel;
          this.elementRef.nativeElement.style.marginLeft = (this.deltasize * this.thumbnailSize) + 'px';
        }
      );



  }

}
