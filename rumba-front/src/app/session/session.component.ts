import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  activatedHelp: boolean = true;

  constructor() { }

  ngOnInit() {
  }

  setHelpStatus() {
    this.activatedHelp = !this.activatedHelp;
  }



}
