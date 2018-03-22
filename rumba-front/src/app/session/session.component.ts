import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { SessionService } from './session.service';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  activatedHelp: boolean = true;
  audioStatus: boolean = false;

  constructor(private sessionSrv: SessionService) { }

  ngOnInit() {
  }

  setHelpStatus() {
    this.activatedHelp = !this.activatedHelp;
  }

  setAudioStatus() {
    this.audioStatus = !this.audioStatus;
  }

  onSubmit(form: NgForm) {
    // console.log('submitted');
    // console.log(form.value);

    this.sessionSrv.startSession(form.value)
      .subscribe(
        (response) => console.log('response::', response),
        (error) => console.log('error::',error)
      );

  }


}
