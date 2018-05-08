import { Component, OnInit } from '@angular/core';
import { Video } from '../model/video.model';
import { VideosServiceService } from '../videos-service.service';

import * as FileSaver from 'file-saver';
import { ToasterService } from 'angular5-toaster/dist/src/toaster.service';

@Component({
  selector: 'app-videos',
  templateUrl: './videos.component.html',
  styleUrls: ['./videos.component.css'],
  providers: [VideosServiceService]
})
export class VideosComponent implements OnInit {
  activatedHelp:boolean = false;
  allVideos: any = undefined;
  allThumbnails: any[] = [];
  thumbsToShow: any[] = [];
  singleVideo: any;

  constructor(private videoService: VideosServiceService, private toasterService: ToasterService) { }

  popToast() {
    this.toasterService.pop('success', 'This is the Title', 'This is the body Body');
    this.toasterService.pop('info', 'This is the Title', 'This is the body Body');
    this.toasterService.pop('warning', 'This is the Title', 'This is the body Body');
    this.toasterService.pop('error', 'This is the Title', 'This is the body Body');
  }

  setHelpStatus():void {
    this.activatedHelp = !this.activatedHelp;
  }

  createImageFromBlob(image: Blob):void {
     let reader = new FileReader();
     reader.addEventListener("load", () => {
        this.thumbsToShow.push(reader.result);
     }, false);

     if (image) {
        reader.readAsDataURL(image);
     }
  }


  ngOnInit() {
    // this.allVideos = this.videoService.getVideos();
    this.videoService.getRecordedVideos()
      .subscribe(
        (response) => {
          this.allVideos = response;

          this.allVideos.forEach((each, index) => {
            // this.getVideoFirstThumbnail(each.video_id);

            this.videoService.getVideoFirstThumb(each.video_id)
              .subscribe(
                (response) => {
                  console.log(response);
                  //this.allThumbnails.push(response['_body']);
                  this.createImageFromBlob(response['_body']);
                }
              );

          });

        }
      );
  }

  downloadVideo(blob: Blob, name: string): void {

    let reader = new FileReader();

    reader.addEventListener("load", () => {
      this.singleVideo = reader.result;
    }, false);

    if (blob) {
       reader.readAsDataURL(blob);
    }

    // download zip file
    FileSaver.saveAs(blob, name);
  }

  onSelectVideo(index:number): void {
    console.log('selectedVideo::::', this.allVideos[index]);
    this.videoService.getSelectedVideo(this.allVideos[index].video_id)
      .subscribe(
        (response) => {
          console.log('this is the selected video', response);

          this.downloadVideo(response, this.allVideos[index].video_name);

        },
        (error) => {
          console.log(error);
        }
      );
  }





}
