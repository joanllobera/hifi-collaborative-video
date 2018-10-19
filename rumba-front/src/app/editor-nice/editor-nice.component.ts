import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DomSanitizer} from '@angular/platform-browser';
import * as JSZip from 'jszip';
import { VideosServiceService } from '../videos-service.service';

import * as FileSaver from 'file-saver';
import { ToasterService } from 'angular5-toaster/dist/src/toaster.service';
import { EditorService } from '../editor.service';
import { TimerObservable } from 'rxjs/observable/TimerObservable';
import { HttpResponse } from '@angular/common/http';
import { Subject } from 'rxjs/Subject';


@Component({
  selector: 'app-editor-nice',
  templateUrl: './editor-nice.component.html',
  styleUrls: ['./editor-nice.component.css']
})
export class EditorNiceComponent implements OnInit {

  lastThumbPos: number = null;
  initialRange = 5;
  oldValue: number = null;
  singleList: string[] = [];
  listOfLists: any[] = [];
  allVideos: any = undefined;
  delta: number[] = [];
  allVideosOk: any[] = [];
  session_id: string[] = [];

  videoJson: any[] = [];
  videoStream: any = undefined;
  zipList: any[] =  [];

  videoZoomValues: number[] = [30, 10, 5, 2, 1];
  whiteSpace: boolean = false;

  pollInterval: number = 9000;
  activePoll: boolean = true;
  sendVideo: boolean = true;
  videoId: string = undefined;
  showSpinner: boolean = false;

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
    // this.startPolling();
  }

  startPolling() {
    TimerObservable.create(0, this.pollInterval)
      .takeWhile(() => this.activePoll)
      .subscribe(() => {
        // alert('EDITOR POLLING');

        // this.sessionService.getVideoWhenReady()
        //   .subscribe((data) => {
        //
        //   });
      });
  }

  unMarcAll() {
    const videoImages = document.querySelectorAll('.iframe span img');
    [].forEach.call(videoImages, (each, index) => {
      if (each.classList.contains('selectedImg')) {
        each.classList.remove('selectedImg');
      }
      if (each.classList.contains('first')) {
        each.classList.remove('first');
      }
      if (each.classList.contains('last')) {
        each.classList.remove('last');
      }
      if (each.classList.contains('orange')) {
        each.classList.remove('orange');
      }
    });
    this.videoJson = [];
  }

  getZoomLevel(slider: number) {
    const values: number[] = [30, 10, 5, 2, 1];
    return values[slider - 1];
  }

  changeZoom(value: number) {
    const values: number[] = [30, 10, 5, 2, 1];
    this.editorSrv.newZoomValue.next(values[value - 1]);
    this.removeClass('orange');
    if (value < this.initialRange) {
      this.recoverThumbnails(value);
    } else {
      // when user is zooming out
     this.recoverThumbnailsZoomOut(value);
    }
    this.oldValue = this.initialRange;
    this.initialRange = value;
  }

  recoverThumbnailsZoomOut(value: number) {
    const iframe = document.querySelectorAll('.iframe');
    const imagesByVideo = [];
    [].forEach.call(iframe, (each, index) => {
      const id = each.id;
      const images = document.querySelectorAll(`#${id} img`);
      imagesByVideo.push(images);
    });
    const newModul = this.getZoomLevel(value);
    const oldModul = this.getZoomLevel(this.oldValue);

    // this.selectUncollapsedIframes(imagesByVideo[1], oldModul, newModul);
  }

  selectUncollapsedIframes(singleArray, oldzoom: number, zoom: number) {
    for (let i = 0; i < singleArray.length; i = i + oldzoom) {
      console.log('current i', i);
      let isSelected: boolean = null;
      for (let k = 0; k < zoom; k++) {
        console.log('current k', k);
        console.log('current k+i', k + i);
        if (i + k === singleArray.length) {
          break;
        }
        if (k === 0) {
          isSelected = singleArray[i + k].classList.contains('selectedImg');
        } else {
          if (isSelected) {
            if (!singleArray[i + k].classList.contains('selectedImg')) {
              singleArray[i + k].classList.add('selectedImg');
            }
          }
        }
        console.log(singleArray[i + k]);
        console.log('--------------------------------------------------------');
      } // end 2ond loop
    } // end 1rst loop
  }

  recoverThumbnails(value: number) {
    const iframe = document.querySelectorAll('.iframe');
    const videoImages = document.querySelectorAll('.iframe span img');
    const numVideos = iframe.length;
    const imagesByVideo = [];
    [].forEach.call(iframe, (each, index) => {
      const id = each.id;
      const images = document.querySelectorAll(`#${id} img`);
      imagesByVideo.push(images);
    });
    const modul = this.getZoomLevel(value);

    this.iterateAllNodeLists(imagesByVideo, modul);
  }

  iterateAllNodeLists(nodeLists, modul) {
    this.whiteSpace = false;
    nodeLists.forEach(currentItem => {
      this.getAllAreSame(currentItem, modul);
    });
    if (this.whiteSpace) {
      this.toasterService.pop(
      'warning',
      `Zoom: ${ this.videoZoomValues[this.initialRange - 1] } seg x thumb`,
      'Hi ha frames sense video en aquest nivell de zoom'
      );
    }
  }

  getAllAreSame(singleArray, zoom: number) {
    for (let i = 0; i < singleArray.length; i = i + zoom) {
      // console.log('currentI', i);
      let isSelected: boolean = null;
      for (let j = 0; j < zoom; j++) {
        if (i + j === singleArray.length) {
          break;
        }
        if (j === 0) {
          isSelected = singleArray[i + j].classList.contains('selectedImg');
        } else {
          if (singleArray[i + j].classList.contains('selectedImg') !== isSelected) {
            // singleArray[i].classList.remove('selectedImg');
            singleArray[i].classList.add('orange');
            this.whiteSpace = true;
            break;
          }
        }
      }
    }
  }

  removeClass(className) {
    const thumbnails = document.querySelectorAll('.iframe span img');
    [].forEach.call(thumbnails, (each, index) => {
      each.classList.remove(className);
    });
  }

  getAllVideos(session_id): void {
    this.listOfLists = [];
    this.videoService.getAllVideos(session_id)
      .subscribe(
        (response) => {
          // console.log(response);
          this.allVideos = response;
          this.allVideosOk = this.allVideos.filter(function (each, index) {
            return each.ts > 0;
          });

          this.allVideosOk.forEach((each, index) => {
            // console.log('eachVideo :::' + index, each);
            if (index > 0) {
              const dif = each.ts - this.allVideosOk[index - 1].ts;
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
            // this.onGetThumbnailsManySync(each.video_id);
          });
          // console.log('this.delta:::', this.delta);
        }
      );
  }

  duplicates(arr, obj): boolean {
    return arr.some(function (each, index) {
      // return each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position;
      return each.id === obj.id && each.thumb === obj.thumb;
    });
  }

  isInArray(arr, obj): boolean {
    return arr.includes(obj);
  }

  getDuplicatedObject(arr, obj): object[] {
    return arr.filter(function (each, index) {
      return each.id === obj.id && each.thumb === obj.thumb;
    });
  }

  getDuplicateIndex(arr, obj): number {
    let _index = null;
    arr.forEach(function(each, index) {
      if (each.id === obj.id && each.thumb === obj.thumb) {
        _index = index;
      }
    });
    return _index;
  }

  isFirstItem(array, object) {
    let first: boolean = true;
    array.forEach((each, index) => {
      if (each.thumb < object.thumb && each.id === object.id) {
        first = false;
      }
    });
    return first;
  }

  isLastItem(array, object) {
    let last: boolean = true;
    array.forEach((each, index) => {
      if (each.thumb > object.thumb && each.id === object.id) {
        last = false;
      }
    });
    return last;
  }

  selectThumbnails (event, videoIndex: number, blobIndex: number, marginDelta: number) {
    if (this.initialRange == 5) {
      this.getThumbInfo(event, videoIndex, blobIndex, marginDelta);
      this.onSelectFrame(event, videoIndex);
    } else  {
      const secondsGap = this.getZoomLevel(this.initialRange);

      const videoId = '#test' + videoIndex + ' img';
      const videoImages = document.querySelectorAll(videoId);
      console.log(videoImages);

      // [].forEach.call(videoImages, (each, index) => {
      //   if (index >= blobIndex && index < blobIndex + secondsGap) {
      //     this.getThumbInfo(each, videoIndex, blobIndex, marginDelta);
      //     this.onSelectFrameIMG(each, videoIndex);
      //   }
      // });

      for (let q = 0; q < secondsGap; q++) {
        videoImages[blobIndex + q].classList.add('selectedImg');
      }


    }
  }

  getThumbInfo(event, videoIndex: number, blobIndex: number, marginDelta: number): void {
    let pos: number;
    // const posWithDelta = Math.trunc( ((event['clientX'] - marginDelta) - 10) / (8 * 10) );
    if (event['clientX']) {
      pos = Math.trunc((event['clientX'] - 10) / (8 * 10));
      this.lastThumbPos = pos;
    } else {
      if (event.x !== 0) {
        pos = Math.trunc((event.x - 10) / (8 * 10));
      } else {
        pos = this.lastThumbPos + 1;
      }
    }

    const thumbnail = {
      id: this.allVideosOk[videoIndex].video_id,
      thumb: blobIndex,
      position: pos
    };
    if (this.isFirstItem(this.videoJson, thumbnail) || this.videoJson.length === 0) {
      const video = document.querySelector('#test' + videoIndex);
      const img = video.querySelector('img.first');
      if (img) {
        img.classList.remove('first');
      }
      if (event.target) {
        event.target.classList.add('first');
      } else {
        event.classList.add('first');
      }
    }
    if (this.isLastItem(this.videoJson, thumbnail) || this.videoJson.length === 0) {
      const video = document.querySelector('#test' + videoIndex);
      const img = video.querySelector('img.last');
      if (img) {
        img.classList.remove('last');
      }
      if (event.target) {
        event.target.classList.add('last');
      } else {
      event.classList.add('last');
      }
    }
    console.log('this.duplicates:::', this.duplicates(this.videoJson, thumbnail));
    if (this.duplicates(this.videoJson, thumbnail)) {
      // remove duplicates
      const removeme = this.getDuplicatedObject(this.videoJson, thumbnail);
      const index = this.getDuplicateIndex(this.videoJson, removeme[0]);
      this.videoJson.splice(index, 1);
    } else {
      this.videoJson.push(thumbnail);
    }
    console.log('videoJson length:::', this.videoJson.length);
  }

  onSelectFrameIMG(img, videoIndex: number): void {
    img.classList.toggle('selectedImg');

    if (img.classList.contains('first') && !img.classList.contains('selectedImg')) {
      img.classList.remove('first');
    }
    const video = document.querySelector('#test' + videoIndex);
    const image = video.querySelector('img.selectedImg');
    if (image) {
      image.classList.add('first');
    }
    if (img.classList.contains('last') && !img.classList.contains('selectedImg')) {
      img.classList.remove('last');
    }
    const imgLast = video.querySelectorAll('img.selectedImg');
    if (imgLast.length > 0) {
      imgLast[imgLast.length-1].classList.add('last');
    }
  }

  onSelectFrame(event, videoIndex: number): void {
    event.target.classList.toggle('selectedImg');

    if (event.target.classList.contains('first') && !event.target.classList.contains('selectedImg')) {
      event.target.classList.remove('first');
    }
    const video = document.querySelector('#test' + videoIndex);
    const img = video.querySelector('img.selectedImg');
    if (img) {
      img.classList.add('first');
    }
    if (event.target.classList.contains('last') && !event.target.classList.contains('selectedImg')) {
      event.target.classList.remove('last');
    }
    const imgLast = video.querySelectorAll('img.selectedImg');
    if (imgLast.length > 0) {
      imgLast[imgLast.length-1].classList.add('last');
    }
  }

  onGetThumbnails(id:string): void {
    this.singleList = [];
    this.videoService.getThunmbnailsFromVideo(id)
      .subscribe(
        (response) => {
          const new_zip = new JSZip();
          new_zip.loadAsync(response)
          .then(
            (zip) => {
              const zipFiles = zip.files;
              const ordered = {};
              Object.keys(zipFiles).sort().forEach(function(key) {
                ordered[key] = zipFiles[key];
              });
              for (const prop in ordered) {
                if (ordered.hasOwnProperty(prop)) {
                  const blob = new Blob( [ ordered[prop]._data.compressedContent ], { type: 'image/jpeg' } );
                  const reader = new FileReader();
                  reader.addEventListener('load', () => {
                    if (reader.result !== '') {
                      this.singleList.push(reader.result);
                    }
                  }, false);
                  if (blob) {
                    reader.readAsDataURL(blob);
                  }
                }
              }
            });
          // download zip file. Do not remove.
          // let fileName = "QCPReport.zip";
          // FileSaver.saveAs(response, fileName);
        },
        (error) => {
          console.log('error::::', error);
        }
      );
  }

  onGetThumbnailsMany(id:string): void {
    const temp = [];
    this.videoService.getThunmbnailsFromVideo(id)
      .subscribe(
        (response) => {
          const new_zip = new JSZip();
          new_zip.loadAsync(response)
          .then(
            (zip) => {
              const zipFiles: any = zip.files;
              const ordered = {};
              Object.keys(zipFiles).sort().forEach(function(key) {
                ordered[key] = zipFiles[key];
              });
              for (const prop in ordered) {
                if (ordered.hasOwnProperty(prop)) {
                  const blob = new Blob( [ ordered[prop]._data.compressedContent ], { type: 'image/jpeg' } );
                  const reader = new FileReader();
                  reader.addEventListener('load', () => {
                    if (reader.result !== '') {
                      temp.push(reader.result);
                    }
                  }, false);
                  if (blob) {
                    reader.readAsDataURL(blob);
                  }
                }
              }
              this.listOfLists.push(temp);
          });
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
          const new_zip = new JSZip();
          const a = new_zip.loadAsync(response)
          .then(
            (zip, index) => {
              // return zip.files;
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
    if (this.videoJson.length === 0) {
      this.toasterService.pop('info', 'Crear Video', 'No hi ha cap thumbnail sel·leccionat.');
      return;
    }
    // this.videoService.buildVideo(this.videoJson, this.session_id)
    //   .subscribe(
    //     (response) => {
    //       this.createVideoFromBlob(response); // httpClient
    //       this.toasterService.pop('success', 'Dades enviades', 'Les dades s\'han enviat correctament.');
    //     }, (error) => {
    //       console.log(error);
    //        if (error.status === 409) {
    //          this.toasterService.pop('error', 'Sessió oberta', 'És necessari tancar la sessió per poder editar el video.');
    //        }
    //     }
    //   );

      this.videoService.sendVideoToBuild(this.videoJson, this.session_id)
        .subscribe(
          (response: HttpResponse<Object>) => {
            console.log(response);
            if (response['status'] === 202) {
              this.videoId = response['body']['videoID'];
              this.toasterService.pop('info', 'Processant video', 'Dades enviades correctament');
              this.showSpinner = true;
            }

            TimerObservable.create(5, this.pollInterval)
            .takeWhile(() => this.activePoll)
            .subscribe(() => {
              this.videoService.getVideoIsReady(this.videoId)
                .subscribe(
                  (response) => {
                    if (response['status'] === 200) {
                      console.log('Video retrieved');
                      this.createVideoFromBlob(response['body']); // httpClient
                      // this.toasterService.pop('success', 'Dades enviades', 'Les dades s\'han enviat correctament.');
                      this.activePoll = false;
                      this.showSpinner = false;
                    } else {
                      console.log('Video not ready');
                    }
                  }, (error) => {
                    console.log(error);
                  });
                });
          }, (error) => {
            if (error.status === 409) {
              this.toasterService.pop('error', 'Sessió oberta', 'És necessari tancar la sessió per poder editar el video.');
            }
          });

  }

  createVideoFromBlob(video: Blob) {
     const reader = new FileReader();
     reader.addEventListener('load', () => {
        this.videoStream = this.sanitizer.bypassSecurityTrustResourceUrl(reader.result);
     }, false);
     if (video) {
        reader.readAsDataURL(video);
     }
  }

}
