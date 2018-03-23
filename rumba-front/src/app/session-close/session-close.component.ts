import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-session-close',
  templateUrl: './session-close.component.html',
  styleUrls: ['./session-close.component.css']
})
export class SessionCloseComponent implements OnInit {

  sessionId: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.sessionId = this.route.snapshot.params['id'];
    console.log('this.sessionId::', this.sessionId);
  }

}
