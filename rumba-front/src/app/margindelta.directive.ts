import { Directive, Input, ElementRef, OnInit } from '@angular/core';
import { VideosServiceService } from './videos-service.service';
import { ZoomLevel } from './zoom-level.pipe';
import { EditorService } from './editor.service';

@Directive({
  selector: '[appMargindelta]'
})
export class MargindeltaDirective implements OnInit {

  @Input() deltasize: number;
  thumbnailSize: number; // size in pixels of the thumbnail in html view


  constructor(
    private elementRef: ElementRef,
    private videoSrv: VideosServiceService,
    private editorSrv: EditorService) { }

  ngOnInit() {
    this.elementRef.nativeElement.style.marginLeft = ((this.deltasize * (8 * 10)) / 1) + 'px';

    this.editorSrv.newZoomValue
      .subscribe(
        (data: number) => {
          this.elementRef.nativeElement.style.marginLeft = ((this.deltasize * (8 * 10)) / data) + 'px';
        }
      );

    this.elementRef.nativeElement.style.marginLeft = (this.deltasize * (8 * 10)) + 'px';

    // this.videoSrv.rangeValue
    //   .subscribe(
    //     (zoomLevel: number) => {
    //       this.thumbnailSize = 8 * zoomLevel;
    //       this.elementRef.nativeElement.style.marginLeft = (this.deltasize * this.thumbnailSize) + 'px';
    //     }
    //   );
  }

  getZoomLevel(slider: number) {
    const values: number[] = [30, 10, 5, 2, 1];
    return values[slider - 1];
  }



}
