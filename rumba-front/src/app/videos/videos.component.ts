import { Component, OnInit } from '@angular/core';
import { Video } from '../model/video.model';
import { VideosServiceService } from '../videos-service.service';

@Component({
  selector: 'app-videos',
  templateUrl: './videos.component.html',
  styleUrls: ['./videos.component.css'],
  providers: [VideosServiceService]
})
export class VideosComponent implements OnInit {

  allVideos: any = [];

  constructor(private videoService: VideosServiceService) { }

  ngOnInit() {
    // this.allVideos = this.videoService.getVideos();
    this.videoService.getRecordedVideos()
      .subscribe(
        (response) => {
          this.allVideos = response;

          this.allVideos.forEach(function (each, index) {
            this.getVideoThumbnail(each.id);
          });

        }
      );
  }

  getVideoThumbnail(videoId:string) {
    this.videoService.getVideoThumbnail(videoId)
      .subscribe(
        (response) => {
          console.log(response);
        }
      );
  }


}
