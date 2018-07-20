import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SessionService } from '../session/session.service';

import { Vimeo } from '../model/vimeo.model';

import * as moment from 'moment';

import { ClipboardModule } from 'ngx-clipboard';
import { ToasterService } from 'angular5-toaster/dist/src/toaster.service';
import { ToasterConfig } from 'angular5-toaster/dist/src/toaster-config';

@Component({
  selector: 'app-session-close',
  templateUrl: './session-close.component.html',
  styleUrls: ['./session-close.component.css']
})
export class SessionCloseComponent implements OnInit {

  activatedHelp: boolean = false;
  sessionId: string;
  binaryData = null;
  vimeouser: string = undefined;
  vimeopassword: string = undefined;
  formatedDate: string = 'undefined';
  editorLink: string = undefined;
  recordLink: string = undefined;

  currentSession: {concert: string, band: string, date:number, is_public: boolean, location: string, vimeo: Vimeo} = undefined;
  public toasterconfig : ToasterConfig = new ToasterConfig({animation: 'fade'});

  isImageLoading: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private sessionSrv: SessionService,
    private router: Router,
    private toasterService: ToasterService) { }

  imageToShow: any;

  createImageFromBlob(image: Blob) {
     let reader = new FileReader();
     reader.addEventListener("load", () => {
        this.imageToShow = reader.result;
     }, false);

     if (image) {
        reader.readAsDataURL(image);
     }
  }



  setHelpStatus() {
    this.activatedHelp = !this.activatedHelp;
  }

  ngOnInit() {
    this.sessionId = this.route.snapshot.params['id'];
    // console.log('this.sessionId::', this.sessionId);

    this.sessionSrv.getSessionById(this.sessionId)
      .subscribe(
        (response) => {
          console.log(response);
          this.currentSession = response.json();

          let dateOk = new Date(this.currentSession.date);
          let niceDate = moment(dateOk).locale('es').format('L');

          this.formatedDate = niceDate;
          // this.vimeouser = this.currentSession.vimeo['username'];
          // this.vimeopassword = this.currentSession.vimeo['password'];
          this.editorLink = this.currentSession['edition_url'];
          this.recordLink = this.currentSession['record_url'];


          this.toasterService.pop('success', 'Crear sessió', 'Sessió creada correctament');

        }
      );

    this.sessionSrv.getLogoById(this.sessionId)
      .subscribe(
        (response) => {
          console.log('getLogoById::', response);
          // this.binaryData = response['_body'];
          this.binaryData = response.blob();
          this.createImageFromBlob(this.binaryData);
        }
      )
  }

  goToMasterCamera() {
    //this.router.navigate([this.currentSession['master_url']]);
    window.open(
      this.currentSession['master_url'],
      '_blank' // <- This is what makes it open in a new window.
    );
  }

  onCloseSession() {
    this.sessionSrv.closeSession(this.sessionId)
      .subscribe(
        (response) => {
          console.log('close session', response);
          this.router.navigate(['/session']);
        }
      )
  }

  onCopyToClipboard() {
    console.log("Edition link saved to clipboard.");
    this.toasterService.pop('info', 'Enllaç creat', 'l\'Enllaç s\'ha copiat al portaretalls');
  }

  onCopyRecordLinkToClipboard() {
    this.toasterService.pop('info', 'Enllaç creat', 'l\'Enllaç s\'ha copiat al portaretalls');
  }

}
