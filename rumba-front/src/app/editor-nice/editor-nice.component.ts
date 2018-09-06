import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DomSanitizer, SafeResourceUrl, SafeUrl} from '@angular/platform-browser';
import * as JSZip from 'jszip';
import { VideosServiceService } from '../videos-service.service';

import * as FileSaver from 'file-saver';
import { ToasterService } from 'angular5-toaster/dist/src/toaster.service';
import { EditorService } from '../editor.service';

@Component({
  selector: 'app-editor-nice',
  templateUrl: './editor-nice.component.html',
  styleUrls: ['./editor-nice.component.css']
})
export class EditorNiceComponent implements OnInit {

  initialRange: number = 10;
  singleList: string[] = [];
  listOfLists: any[] = [];
  allVideos: any = undefined;
  delta: number[] = [];
  allVideosOk: any[] = [];
  session_id: string[] = [];

  videoJson: any[] = [];
  videoStream: any = undefined;
  zipList: any[] =  [];

  @ViewChild('videoList') videoList: ElementRef;
  @ViewChild('iframe') iframe: ElementRef;

  constructor(
    private videoService: VideosServiceService,
    private sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    private toasterService: ToasterService,
    private videoSrv: VideosServiceService,
    private editorSrv: EditorService) {

    this.route.params.subscribe(res => this.session_id = res.session_id);
  }

  ngOnInit() {
    this.getAllVideos(this.session_id);
    // this.onGetThumbnails("5ad4b5fdc94b4c6bc260dd3c");
  }

  changeZoom(value: number) {
    this.videoSrv.rangeValue.next(value);
    this.initialRange = value;
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

            if (index === 0) {
              this.onGetThumbnailsMany(each.video_id);
            } else {
              setTimeout(() => {
                this.onGetThumbnailsMany(each.video_id);
              }, 2000);
            }



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

  isFirst(array, object) {
    return array.every(function (each, index) {
      return object.position < each.position;
    })
  }

  getThumbInfo(event, videoIndex: number, blobIndex: number): void {

    let pos = Math.trunc((event['clientX'] - 7) / 80);
    // console.log("event['clientX']:::", event['clientX']);
    // console.log("pos:::", pos);

    let thumbnail = {
      id: this.allVideosOk[videoIndex].video_id,
      thumb: blobIndex,
      position: pos
    };

    if (this.isFirst(this.videoJson, thumbnail) || this.videoJson.length === 0) {
      let video = document.querySelector('#test' + videoIndex);
      let img = video.querySelector('img.first');
      if (img) img.classList.remove('first');

      event.target.classList.add('first');
    }

    if (this.duplicates(this.videoJson, thumbnail)) {
      //remove duplicates
      let removeme = this.getDuplicatedObject(this.videoJson, thumbnail);
      let index = this.getDuplicateIndex(this.videoJson, removeme[0]);
      this.videoJson.splice(index, 1);
    } else {
      this.videoJson.push(thumbnail);
    }
    console.log(this.videoJson);
  }

  onSelectFrame(event, videoIndex: number, blobIndex: number): void {
    event.target.classList.toggle('selectedImg');
    if (event.target.classList.contains('first') && !event.target.classList.contains('selectedImg')) {
      event.target.classList.remove('first');
    }

    let video = document.querySelector('#test' + videoIndex);
    let img = video.querySelector('img.selectedImg');
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

          // console.log('zip.files::::::::', a);

        },
        (error) => {
          // console.log('error::::', error);
        }
      );

  }


  sendVideoToServer() {
    this.videoService.buildVideo(this.videoJson, this.session_id)
      .subscribe(
        (response) => {
          this.createVideoFromBlob(response); //httpClient
          this.toasterService.pop('success', 'Dades enviades', 'Les dades s\'han enviat correctament.');
        }, (error) => {
          console.log(error);
           if (error.status === 409) {
             this.toasterService.pop('error', 'Sessió oberta', 'És necessari tancar la sessió per poder editar el video.');
           }
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
