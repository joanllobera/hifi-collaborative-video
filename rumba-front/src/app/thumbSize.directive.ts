import { Directive, OnInit, ElementRef } from "@angular/core";
import { VideosServiceService } from "./videos-service.service";


@Directive({
  selector: '[appThumbSize]'
})
export class ThumbSizeDirective implements OnInit {

  currentWidth: number = 80;

  constructor(private elementRef: ElementRef, private videoSrv: VideosServiceService) {}

  ngOnInit(): void {
    this.videoSrv.rangeValue
      .subscribe(
        (value: number) => {
          this.currentWidth = value;
          this.elementRef.nativeElement.style.width = (8 * this.currentWidth) + 'px';
        }
      );
  }

}
