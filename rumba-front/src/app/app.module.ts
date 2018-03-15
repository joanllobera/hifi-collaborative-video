import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing-module';


import { AppComponent } from './app.component';
import { StylesComponent } from './styles/styles.component';

@NgModule({
  declarations: [
    AppComponent,
    StylesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
