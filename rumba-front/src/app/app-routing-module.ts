import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StylesComponent } from './styles/styles.component';
import { SessionComponent } from './session/session.component';
import { HomeComponent } from './home/home.component';
import { OrientationComponent } from './orientation/orientation.component';
import { VideosComponent } from './videos/videos.component';
import { SessionCloseComponent } from './session-close/session-close.component';
import { CameraComponent } from './camera/camera.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'orientation', component: OrientationComponent},
  { path: 'styles', component: StylesComponent },
  { path: 'session', component: SessionComponent },
  { path: 'sessionClose/:id', component: SessionCloseComponent},
  { path: 'videos', component: VideosComponent },
  { path: 'camera', component: CameraComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes)
  ],
  exports: [RouterModule]
})

export class AppRoutingModule {

}
