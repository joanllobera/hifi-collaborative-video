import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { RecordService } from  '../record.service';
import { Observable } from  'rxjs/Observable';
import { Observer } from 'rxjs';
import * as $ from 'jquery';
import '../../assets/serverdate/ServerDate.js';
import { AppConfig } from '../app-config';

declare var Janus: any;
declare var ServerDate: any;

@Component({
  selector: 'app-camera-back',
  templateUrl: './camera-back.component.html',
  styleUrls: ['./camera-back.component.css']
})
export class CameraBackComponent implements OnInit {

  isRecording: boolean = false;
  videoPath: any = undefined;
  videoId: string = undefined;
  @ViewChild('fullVideo') videoElem: ElementRef;
  fullScreen: boolean = false;
  allowRecording: boolean = false;

  constructor(private record: RecordService) { }

  ngOnInit() {
  }

  toggleFullScreen() {
    // document.documentElement.webkitRequestFullScreen();
    this.fullScreen = true;

    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    } else if (document.documentElement.webkitRequestFullscreen) {
      document.documentElement.webkitRequestFullScreen();
    }

  }

  exitFullScreen() {
    //document.webkitExitFullscreen();
    this.fullScreen = false;

    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }


  }

  checkButton() {
    this.isRecording = !this.isRecording;
  }

  startRecording() {
    this.record.startRecordingVideo()
      .subscribe(
        (response) => {
          console.log(response);
          this.videoPath = response['video_path'];
          this.videoId = response['id'];
          this.configureJanus(this.videoPath);

        }
      )
  }

  stopRecording() {
    this.record.stopRecordingVideo(this.videoId)
      .subscribe(
        (response) => {
          console.log(response);
        }
      )
  }



  // Helper to parse query string
  getQueryStringValue(name) {
  	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  	var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
  		results = regex.exec(location.search);
  	return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }


  configureJanus(videoPath: string) {

    var server = AppConfig.JANUS_DEV;

    var janus = null;
    var echotest = null;
    var opaqueId = "devicetest-"+Janus.randomString(12);

    var started = false, firstTime = true;
    var bitrateTimer = null;
    var spinner = null;

    var audioDeviceId = null;
    var videoDeviceId = null;

    var audioenabled = false;
    var videoenabled = false;

    var doSimulcast = (this.getQueryStringValue("simulcast") === "yes" || this.getQueryStringValue("simulcast") === "true");
    var simulcastStarted = false;

	function calculate_time_delta(n_reqs){
		var timedelta = 0;
		var i;
		for (i=0; i< n_reqs; i++){
			timedelta += Math.round(ServerDate.now() - Date.now());
		}
		return timedelta;
	}

    // Helper method to prepare a UI selection of the available devices
    function initDevices(devices) {
      var deviceList = [];
    	devices.forEach(function(device) {

        if (device.kind === 'videoinput') {
          console.log('device::::', device);
          deviceList.push(device);
        }

    	});

    	restartCapture(deviceList);
    }

    function restartCapture(deviceList) {
        var iidd = undefined;
        if (deviceList.length > 1) {
            deviceList.forEach(function(each){
              if (each.label.match('back')) {
                iidd = each.deviceId;
              }
            });

          // iidd = deviceList[1].deviceId;
        } else {
          iidd = deviceList[0].deviceId;
        }
		// Starting ServerDate synchronization on attachment success
		var n_reqs = 30;
	    var timedelta = 0;
	    while (timedelta === 0){
	    	timedelta = calculate_time_delta(n_reqs);
	    }
	    var delta = timedelta / n_reqs;

      	// Negotiate WebRTC
      	var body = { "audio": true, "video": true, "timedelta": delta, "filename": videoPath};
      	Janus.debug("Sending message (" + JSON.stringify(body) + ")");
      	echotest.send({"message": body});
      	Janus.debug("Trying a createOffer too (audio/video sendrecv)");
      	var replaceAudio = false;
      	var replaceVideo = true;
      	echotest.createOffer(
      		{
      			// We provide a specific device ID for both audio and video
      			media: {
      				audio: false,
      				replaceAudio: replaceAudio,	// This is only needed in case of a renegotiation
      				video: {
      					deviceId: {
      						exact: iidd
      					}
      				},
      				replaceVideo: replaceVideo,	// This is only needed in case of a renegotiation
      				data: true	// Let's negotiate data channels as well
      			},
      			// If you want to test simulcasting (Chrome and Firefox only), then
      			// pass a ?simulcast=true when opening this demo page: it will turn
      			// the following 'simulcast' property to pass to janus.js to true
      			simulcast: doSimulcast,
      			success: function(jsep) {
      				Janus.debug("Got SDP!");
      				Janus.debug(jsep);
      				echotest.send({"message": body, "jsep": jsep});
      			},
      			error: function(error) {
      				Janus.error("WebRTC error:", error);
      			}
      		});
      }


    Janus.init({debug: "all", callback: function() {
		// Use a button to start the demo
			// Make sure the browser supports WebRTC
			if(!Janus.isWebrtcSupported()) {
				return;
			}
			// Create session
			var janus = new Janus(
				{
					server: server,
					success: function() {
						// Attach to echo test plugin
						janus.attach(
							{
								plugin: "janus.plugin.echotest",
								opaqueId: opaqueId,
								success: function(pluginHandle) {
									echotest = pluginHandle;
									Janus.log("Plugin attached! (" + echotest.getPlugin() + ", id=" + echotest.getId() + ")");
									// Enumerate devices: that's what we're here for
									Janus.listDevices(initDevices);
									// We wait for the user to select the first device before making a move
									// $('#start').removeAttr('disabled').html("Stop")
									// 	.click(function() {
									// 		$(this).attr('disabled', "true");
									// 		clearInterval(bitrateTimer);
									// 		janus.destroy();
									// 	});

                  $('#stop').bind('click', function (){
                    janus.destroy();
                  });

								},
								error: function(error) {
									console.error("  -- Error attaching plugin...", error);
								},
								consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");

								},
								onmessage: function(msg, jsep) {
									Janus.debug(" ::: Got a message :::");
									Janus.debug(msg);
									if(jsep !== undefined && jsep !== null) {
										Janus.debug("Handling SDP as well...");
										Janus.debug(jsep);
										echotest.handleRemoteJsep({jsep: jsep});
									}

								},
								onlocalstream: function(stream) {
									Janus.debug(" ::: Got a local stream :::");
									Janus.debug(stream);

                  Janus.attachMediaStream(document.getElementById('myvideo'), stream);

                  document.getElementById('myvideo').setAttribute('muted', "muted");





								},
								onremotestream: function(stream) {
									Janus.debug(" ::: Got a remote stream :::");
									Janus.debug(stream);

								},
								ondataopen: function(data) {
									Janus.log("The DataChannel is available!");

								},
								ondata: function(data) {
									Janus.debug("We got data from the DataChannel! " + data);

								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification :::");
								}
							});
					},
					error: function(error) {
						Janus.error(error);
					},
					destroyed: function() {
						window.location.reload();
            console.log('destroyed');
					}
				});

	}});


  }




}
