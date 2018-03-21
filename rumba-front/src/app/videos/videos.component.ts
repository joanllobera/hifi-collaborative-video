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

  allVideos: Video[] = [];

  constructor(private videoService: VideosServiceService) { }

  ngOnInit() {
    this.allVideos = this.videoService.getVideos();
  }

}
