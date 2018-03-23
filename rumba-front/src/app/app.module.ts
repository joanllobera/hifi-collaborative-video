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




@NgModule({
  declarations: [
    AppComponent,
    StylesComponent,
    HeaderComponent,
    SessionComponent,
    HomeComponent,
    OrientationComponent,
    VideosComponent,
    SessionCloseComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpModule,
    HttpClientModule
  ],
  exports: [
    HeaderComponent
  ],
  providers: [SessionService],
  bootstrap: [AppComponent]
})
export class AppModule { }
