import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { SessionService } from './session.service';


@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  activatedHelp: boolean = false;
  audioStatus: boolean = false;
  selectedFile: any = null;


  constructor(private sessionSrv: SessionService, private router: Router) { }

  ngOnInit() {
  }

  setHelpStatus() {
    this.activatedHelp = !this.activatedHelp;
  }

  setAudioStatus() {
    this.audioStatus = !this.audioStatus;
  }

  onFileSelected(event) {
    this.selectedFile = event.target.files[0];
  }

  onUploadLogo() {

  }

  onSubmit(form: NgForm) {
    form.value.date = (new Date(form.value.date)).getTime();

    if (form.value.is_public == 'true') {
      form.value.is_public = true;
    } else {
      form.value.is_public = false;
    }
    this.sessionSrv.startSession(form.value)
      .subscribe(
        (response) => {
          console.log('response::', response);
          var a = response.json();
          this.router.navigate(['/sessionClose', a.id]);
        },
        (error) => console.log('error::',error)
      );
  }






}
