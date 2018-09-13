import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
  name: 'zoomLevel'
})

export class ZoomLevel implements PipeTransform {
  transform(zoomValue: number, currentIndex: number) {
    return currentIndex % zoomValue == 0;
  }
}
