import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-editor-nice',
  templateUrl: './editor-nice.component.html',
  styleUrls: ['./editor-nice.component.css']
})
export class EditorNiceComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  onSelectFrame(event) {
    event.target.classList.toggle('selectedImg');
  }



}
