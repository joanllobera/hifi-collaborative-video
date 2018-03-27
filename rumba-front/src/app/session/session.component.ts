import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { HttpClient } from '@angular/common/http';

import { SessionService } from './session.service';

import { AppConfig } from '../app-config';


@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  activatedHelp: boolean = false;
  audioStatus: boolean = false;
  selectedFile: File = null;

  constructor(private sessionSrv: SessionService, private router: Router, private http: HttpClient) { }

  ngOnInit() {
  }

  setHelpStatus() {
    this.activatedHelp = !this.activatedHelp;
  }

  setAudioStatus() {
    this.audioStatus = !this.audioStatus;
  }

  onFileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
  }

  onUploadLogo(id: string) {

    this.sessionSrv.uploadLogo(id, this.selectedFile)
      .subscribe(res => {
        console.log(res);
      });
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


          if (this.selectedFile) {
              this.onUploadLogo(a.id);
          }
          this.router.navigate(['/sessionClose', a.id]);
        },
        (error) => {
          console.log('error::',error);
        }
      );
  }






}
