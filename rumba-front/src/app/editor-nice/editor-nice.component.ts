import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';
import * as JSZip from 'jszip';
import { VideosServiceService } from '../videos-service.service';

import * as FileSaver from 'file-saver';

@Component({
  selector: 'app-editor-nice',
  templateUrl: './editor-nice.component.html',
  styleUrls: ['./editor-nice.component.css']
})
export class EditorNiceComponent implements OnInit {

  singleList: string[] = [];
  listOfLists: any[] = [];
  allVideos: any = undefined;
  delta: number[] = [];
  allVideosOk: any[] = [];
  session_id: string[] = [];

  videoJson: any[] = [];
  videoStream: any = undefined;
  zipList: any[] =  [];


  constructor(private videoService: VideosServiceService, private sanitizer: DomSanitizer, private route: ActivatedRoute) {

    this.route.params.subscribe(res => this.session_id = res.session_id);
  }

  ngOnInit() {
    this.getAllVideos(this.session_id);
    // this.onGetThumbnails("5ad4b5fdc94b4c6bc260dd3c");
  }

  getAllVideos(session_id): void {
    this.listOfLists = [];
    this.videoService.getAllVideos(session_id)
      .subscribe(
        (response) => {
          // console.log(response);
          this.allVideos = response;
          this.allVideosOk = this.allVideos.filter(function (each, index) {
            return each.ts > 0
          });

          this.allVideosOk.forEach((each, index) => {
            // console.log('eachVideo :::' + index, each);
            if (index > 0) {
              var dif = each.ts - this.allVideosOk[index-1].ts;
              this.delta.push(dif);
              // console.log('videoNum '+index+' amb dif de ', dif);
            } else {
              this.delta.push(0);
            }

            setTimeout(() => {
              this.onGetThumbnailsMany(each.video_id);
            }, 2000);

            // this.onGetThumbnailsMany(each.video_id); //this works asynchronous


            //this.onGetThumbnailsManySync(each.video_id);


          });
          // console.log('this.delta:::', this.delta);
        }
      );
  }

  duplicates(arr, obj): boolean {
    return arr.some(function (each, index) {
      return each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position;
    })
  }

  duplicatePosition(arr, obj): boolean {
    return arr.some(function(each, index){
      return each.position === obj.position;
    });
  }

  getDuplicatedObject(arr, obj): object[] {
    return arr.filter(function (each, index) {
      return each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position;
    });
  }

  getDuplicatedObjectByPosition(arr, obj): object[] {
    return arr.filter(function (each, index) {
      return each.position === obj.position;
    });
  }

  getDuplicateIndex(arr, obj): number {
    var _index = null;
    arr.forEach(function(each, index){
      if (each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position){
        _index = index;
      }
    });
    return _index;
  }



  getThumbInfo(event: Event, videoIndex: number, blobIndex: number): void {

    var pos = Math.trunc((event['clientX'] - 7) / 80);
    // console.log("event['clientX']:::", event['clientX']);
    // console.log("pos:::", pos);

    var thumbnail = {
      id: this.allVideosOk[videoIndex].video_id,
      thumb: blobIndex,
      position: pos
    };

    if (this.duplicates(this.videoJson, thumbnail)) {

      //remove duplicates
      var removeme = this.getDuplicatedObject(this.videoJson, thumbnail);
      var index = this.getDuplicateIndex(this.videoJson, removeme[0]);
      this.videoJson.splice(index, 1);
    } else {
      if (this.duplicatePosition(this.videoJson, thumbnail)) {
        //buscar el de la misma position y borrarlo
        // let duplicatedByPosition = this.getDuplicatedObjectByPosition(this.videoJson, thumbnail);
        // let index = this.getDuplicateIndex(this.videoJson, duplicatedByPosition[0]);
        // this.videoJson.splice(index, 1);
        alert('Hi ha més d\'un franme sel·leccionat pel mateix període de temps')
        this.videoJson.push(thumbnail);
      } else {
        this.videoJson.push(thumbnail);
      }

    }

    console.log('videoJson::', this.videoJson);
    console.log('event:::', event);
    // console.log('videoIndex:::', videoIndex);
    // console.log('blobIndex:::', blobIndex);
  }

  onSelectFrame(event): void {
    event.target.classList.toggle('selectedImg');
  }

  onGetThumbnails(id:string): void {
    this.singleList = [];
    this.videoService.getThunmbnailsFromVideo(id)
      .subscribe(
        (response) => {
          var new_zip = new JSZip();
          new_zip.loadAsync(response)
          .then(
            (zip) => {

              let zipFiles = zip.files;
              const ordered = {};
              Object.keys(zipFiles).sort().forEach(function(key) {
                ordered[key] = zipFiles[key];
              });


              for (var prop in ordered) {
                let blob = new Blob( [ ordered[prop]._data.compressedContent ], { type: "image/jpeg" } );
                let reader = new FileReader();
                reader.addEventListener("load", () => {
                  if (reader.result != "") {
                    this.singleList.push(reader.result);
                  }
                }, false);
                if (blob) {
                   reader.readAsDataURL(blob);
                }
              }
          });

          // download zip file
          // let fileName = "QCPReport.zip";
          // FileSaver.saveAs(response, fileName);

        },
        (error) => {
          console.log('error::::', error);
        }
      );

  }


  onGetThumbnailsMany(id:string): void {
    var temp = [];
    this.videoService.getThunmbnailsFromVideo(id)
      .subscribe(
        (response) => {
          var new_zip = new JSZip();
          new_zip.loadAsync(response)
          .then(
            (zip) => {
              let zipFiles = zip.files;
              const ordered = {};
              Object.keys(zipFiles).sort().forEach(function(key) {
                ordered[key] = zipFiles[key];
              });

              for (var prop in ordered) {
                let blob = new Blob( [ ordered[prop]._data.compressedContent ], { type: "image/jpeg" } );
                let reader = new FileReader();
                reader.addEventListener("load", () => {
                  if (reader.result != "") {
                    temp.push(reader.result);
                  }
                }, false);
                if (blob) {
                   reader.readAsDataURL(blob);
                }
              }

              this.listOfLists.push(temp);
              console.log('this.listOfLists::::', this.listOfLists);

          });

          // download zip file
          // let fileName = "QCPReport.zip";
          // FileSaver.saveAs(response, fileName);

        },
        (error) => {
          console.log('error::::', error);
        }
      );
  }


  onGetThumbnailsManySync(id:string): void {

    this.videoService.getThunmbnailsFromVideo(id)
      .subscribe(
        (response) => {
          var new_zip = new JSZip();
          var a = new_zip.loadAsync(response)
          .then(
            (zip, index) => {
              //return zip.files;
              this.zipList.push(zip.files);
          });

          console.log('zip.files::::::::', a);

        },
        (error) => {
          console.log('error::::', error);
        }
      );

      console.log('lalalalalalala:::::::', this.zipList);
  }


  sendVideoToServer() {
    this.videoService.buildVideo(this.videoJson, this.session_id)
      .subscribe(
        (response) => {
          this.createVideoFromBlob(response); //httpClient
          // this.createVideoFromBlob(response.blob()); //http
        }, (error) => {
          console.log(error);
        }
      );
  }

  createVideoFromBlob(video: Blob) {
     let reader = new FileReader();
     reader.addEventListener("load", () => {
        this.videoStream = this.sanitizer.bypassSecurityTrustResourceUrl(reader.result);
     }, false);

     if (video) {
        reader.readAsDataURL(video);
     }
  }





}
