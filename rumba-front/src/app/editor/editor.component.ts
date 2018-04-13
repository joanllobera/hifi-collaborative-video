import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.css']
})
export class EditorComponent implements OnInit {

  videos = ['title1', 'title2', 'title3', 'title4', 'title5', 'title6', 'title7', 'title8', 'title9', 'title10'];

  constructor() { }

  ngOnInit() {
  }

  onSelectFrame(event) {
    event.target.classList.toggle('selectedImg');
  }


}
