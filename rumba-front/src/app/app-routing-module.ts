import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StylesComponent } from './styles/styles.component';
import { SessionComponent } from './session/session.component';
import { HomeComponent } from './home/home.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'styles', component: StylesComponent },
  { path: 'sessio', component: SessionComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes)
  ],
  exports: [RouterModule]
})

export class AppRoutingModule {

}
