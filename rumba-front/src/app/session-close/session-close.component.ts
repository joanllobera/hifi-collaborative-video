import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SessionService } from '../session/session.service';


@Component({
  selector: 'app-session-close',
  templateUrl: './session-close.component.html',
  styleUrls: ['./session-close.component.css']
})
export class SessionCloseComponent implements OnInit {

  sessionId: string;
  src: string;

  currentSession: {concert: string, band: string, date:number, is_public: boolean} = undefined;

  constructor(private route: ActivatedRoute, private sessionSrv: SessionService, private router: Router) { }

  ngOnInit() {
    this.sessionId = this.route.snapshot.params['id'];
    // console.log('this.sessionId::', this.sessionId);

    this.sessionSrv.getSessionById(this.sessionId)
      .subscribe(
        (response) => {
          console.log(response);
          this.currentSession = response.json();
        }
      );

    this.sessionSrv.getLogoById(this.sessionId)
      .subscribe(
        (logo) => {
          console.log('getLogoById::', logo);
          
        }
      )



  }

  onCloseSession() {
    this.sessionSrv.closeSession(this.sessionId)
      .subscribe(
        (response) => {
          console.log('close session', response);
          this.router.navigate(['/home']);
        }
      )
  }

}
