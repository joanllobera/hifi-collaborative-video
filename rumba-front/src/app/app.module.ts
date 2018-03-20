import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing-module';


import { AppComponent } from './app.component';
import { StylesComponent } from './styles/styles.component';
import { HeaderComponent } from './header/header.component';
import { SessionComponent } from './session/session.component';
import { HomeComponent } from './home/home.component';
import { OrientationComponent } from './orientation/orientation.component';

@NgModule({
  declarations: [
    AppComponent,
    StylesComponent,
    HeaderComponent,
    SessionComponent,
    HomeComponent,
    OrientationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  exports: [
    HeaderComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
