import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing-module';

import { AppComponent } from './app.component';
import { StylesComponent } from './styles/styles.component';
import { HeaderComponent } from './header/header.component';
import { SessionComponent } from './session/session.component';
import { HomeComponent } from './home/home.component';
import { OrientationComponent } from './orientation/orientation.component';
import { VideosComponent } from './videos/videos.component';

import { SessionService } from './session/session.service';
import { SessionCloseComponent } from './session-close/session-close.component';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { RecordService } from './record.service';
import { CameraBackComponent } from './camera-back/camera-back.component';
import { EditorNiceComponent } from './editor-nice/editor-nice.component';

import { VideosServiceService } from './videos-service.service';
import { MargindeltaDirective } from './margindelta.directive';
import { ClipboardModule } from 'ngx-clipboard';
import { ToasterModule } from 'angular5-toaster/dist/src/toaster.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CameraMasterComponent } from './camera-master/camera-master.component';
import { ThumbSizeDirective } from './thumbSize.directive';
import { SelectorSizeDirective } from './selectorSize.directive';
import { EditorService } from './editor.service';
import { ClaudatorMoveDirective } from './claudator-move.directive';
import { ClaudatorLeftDirective } from './claudator-left.directive';



@NgModule({
  declarations: [
    AppComponent,
    StylesComponent,
    HeaderComponent,
    SessionComponent,
    HomeComponent,
    OrientationComponent,
    VideosComponent,
    SessionCloseComponent,
    CameraBackComponent,
    EditorNiceComponent,
    MargindeltaDirective,
    CameraMasterComponent,
    ThumbSizeDirective,
    SelectorSizeDirective,
    ClaudatorMoveDirective,
    ClaudatorLeftDirective
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ClipboardModule,
    HttpModule,
    HttpClientModule,
    BrowserAnimationsModule,
    ToasterModule,
    NgbModule.forRoot()
  ],
  exports: [
    HeaderComponent
  ],
  providers: [
    SessionService,
    RecordService,
    VideosServiceService,
    EditorService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
