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

  initialRange: number = 5;
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
  }

  getZoomLevel(slider: number) {
    const values: number[] = [30, 10, 5, 2, 1];
    return values[slider - 1];
  }

  changeZoom(value: number) {
    this.initialRange = value;
    this.removeClass('orange');
    this.recoverThumbnails(value);
  }

  recoverThumbnails(value: number) {
    const iframe = document.querySelectorAll('.iframe');
    const videoImages = document.querySelectorAll('.iframe span img');
    const numVideos = iframe.length;
    const imagesByVideo = [];
    [].forEach.call(iframe, (each, index) => {
      console.log('each [][][]::', each);
      const id = each.id;
      const images = document.querySelectorAll(`#${id} img`);
      imagesByVideo.push(images);
      console.log('imagesByVideo:::', imagesByVideo);
    });
    const modul = this.getZoomLevel(value);
    this.getAllAreSame(imagesByVideo[0], modul);
  }

  removeClass(className) {
    const thumbnails = document.querySelectorAll('.iframe span img');
    [].forEach.call(thumbnails, (each, index) => {
      each.classList.remove(className);
    });
  }

  getAllAreSame(singleArray, zoom: number) {
    let whiteSpace: boolan = false;
    for (let i = 0; i < singleArray.length; i = i + zoom) {
      console.log('currentI', i);
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
            whiteSpace = true;
            break;
          }
        }
      }
    }
    if (whiteSpace) {
      this.toasterService.pop(
      'error',
      `Zoom: ${this.videoZoomValues[this.initialRange - 1]} seg x thumbnail`,
      'Hi ha frames sense cap video assignat'
      );
    }
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
              const dif = each.ts - this.allVideosOk[index-1].ts;
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
      return each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position;
    });
  }

  isInArray(arr, obj): boolean {
    return arr.includes(obj);
  }

  getDuplicatedObject(arr, obj): object[] {
    return arr.filter(function (each, index) {
      return each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position;
    });
  }

  getDuplicateIndex(arr, obj): number {
    let _index = null;
    arr.forEach(function(each, index){
      if (each.id === obj.id && each.thumb === obj.thumb && each.position === obj.position){
        _index = index;
      }
    });
    return _index;
  }

  isNotFirst(array, object) {
    return array.some( (each, index) => {
      return each.position < object.position && each.id === object.id;
    });
  }

  isFirstItem(array, object) {
    let first: boolean = true;
    array.forEach((each, index) => {
      if (each.position < object.position && each.id === object.id) {
        first = false;
      }
    });
    return first;
  }

  isLastItem(array, object) {
    let last: boolean = true;
    array.forEach((each, index) => {
      if (each.position > object.position && each.id === object.id) {
        last = false;
      }
    });
    return last;
  }

  isNotLast(array, object) {
    return array.some( (each, index) => {
      return each.position > object.position && each.id == object.id;
    });
  }

  getThumbInfo(event, videoIndex: number, blobIndex: number, marginDelta: number): void {
    const pos = Math.trunc((event['clientX'] - 10) / (8 * 10));
    const posWithDelta = Math.trunc( ((event['clientX'] - marginDelta) - 10) / (8 * 10) );
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
      event.target.classList.add('first');
    }
    if (this.isLastItem(this.videoJson, thumbnail) || this.videoJson.length === 0) {
      const video = document.querySelector('#test' + videoIndex);
      const img = video.querySelector('img.last');
      if (img) {
        img.classList.remove('last');
      }
      event.target.classList.add('last');
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

  onSelectFrame(event, videoIndex: number, blobIndex: number): void {
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
    this.videoService.buildVideo(this.videoJson, this.session_id)
      .subscribe(
        (response) => {
          this.createVideoFromBlob(response); // httpClient
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
     const reader = new FileReader();
     reader.addEventListener('load', () => {
        this.videoStream = this.sanitizer.bypassSecurityTrustResourceUrl(reader.result);
     }, false);
     if (video) {
        reader.readAsDataURL(video);
     }
  }

}
