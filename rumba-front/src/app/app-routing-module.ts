import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StylesComponent } from './styles/styles.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/styles', pathMatch: 'full' },
  { path: 'styles', component: StylesComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes)
  ],
  exports: [RouterModule]
})

export class AppRoutingModule {

}
