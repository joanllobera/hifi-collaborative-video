import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-orientation',
  templateUrl: './orientation.component.html',
  styleUrls: ['./orientation.component.css']
})
export class OrientationComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  getOrientation() {
    if (window.outerWidth > window.outerHeight) {
      alert('landscape');
      return 'landscape';
    }
    alert('portrait');
    return 'portrait';
  }

}
