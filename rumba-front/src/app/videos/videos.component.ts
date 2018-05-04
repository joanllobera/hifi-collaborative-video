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

  allVideos: any = undefined;
  allThumbnails: any[] = [];

  constructor(private videoService: VideosServiceService) { }

  getVideoFirstThumbnail(videoId:string) {
    this.videoService.getVideoFirstThumb(videoId)
      .subscribe(
        (response) => {
          console.log(response);
          this.allThumbnails.push(response);
        }
      );
  }

  ngOnInit() {
    // this.allVideos = this.videoService.getVideos();
    this.videoService.getRecordedVideos()
      .subscribe(
        (response) => {
          this.allVideos = response;

          this.allVideos.forEach(function (each, index) {
            // this.getVideoFirstThumbnail(each.video_id);

            this.videoService.getVideoFirstThumb(each.video_id)
              .subscribe(
                (response) => {
                  console.log(response);
                  this.allThumbnails.push(response);
                }
              );

          });
        }
      );
  }






}
