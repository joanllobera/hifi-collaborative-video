import { Component, OnInit } from '@angular/core';

import { Observable } from  'rxjs/Observable';
import { Observer } from 'rxjs';

import { RecordService } from  '../record.service';


//import '../assets/janus/janus.js';

declare var Janus: any;

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.css']
})
export class CameraComponent implements OnInit {

  isRecording: boolean = false;

  constructor(private record: RecordService) { }

  checkButton() {
    this.isRecording = !this.isRecording;
  }

  startRecording() {
    this.record.startRecordingVideo()
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

  configureJanus() {
    var elem = document.getElementById("myvideo");
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    }
    Janus.init({
     debug: true,
     dependencies: Janus.useDefaultDependencies(),
     callback: function() {
            alert('Janus initialized');

     }
   });
    var echotest = null;
    var opaqueId = "echotest-"+Janus.randomString(12);

    var bitrateTimer = null;
    var spinner = null;

    var audioenabled = false;
    var videoenabled = false;

    var doSimulcast = (this.getQueryStringValue("simulcast") === "yes" || this.getQueryStringValue("simulcast") === "true");
    var simulcastStarted = false;
    var deviceList =[];



  function initDevices(devices) {
  	devices.forEach(function(device) {
        if (device.kind === 'videoinput') {
          console.log('each device:::', device);
          alert(device.deviceId);
          deviceList.push(device);
        }
    });

    if (deviceList.length > 1) {
      restartCapture(deviceList[1].deviceId);
    }


  }

  function restartCapture(iidd) {
  	// Negotiate WebRTC
var body = { "audio": false, "video": true,  };
  	Janus.debug("Sending message (" + JSON.stringify(body) + ")");
  	echotest.send({"message": body});
  	Janus.debug("Trying a createOffer too (audio/video sendrecv)");

  	var videoDeviceId = iidd;

  	echotest.createOffer(
  		{
  			// We provide a specific device ID for both audio and video
  			media: {
  				video: {
  					deviceId: {
  						exact: videoDeviceId
  					}
  				},
  				replaceVideo: true,
          audio:false,	// This is only needed in case of a renegotiation
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

  			}
  		});
}












  var janus = new Janus({
      server: 'https://192.168.10.252:8080/janus',
      success: function() {

              // Done! attach to plugin XYZ
              // Attach to echo test plugin, using the previously created janus instance
              janus.attach({
                plugin: "janus.plugin.echotest",
                success: function(pluginHandle) {
                  Janus.listDevices(initDevices);
                  // Plugin attached! 'pluginHandle' is our handle
                  echotest = pluginHandle;
                  // Negotiate WebRTC
									var body = { "audio": false, "video": true };
									Janus.debug("Sending message (" + JSON.stringify(body) + ")");
									echotest.send({"message": body});
									Janus.debug("Trying a createOffer too (audio/video sendrecv)");
									// echotest.createOffer({
									// 		// No media provided: by default, it's sendrecv for audio and video
									// 		media: {
                  //       video: true,
                  //       audio:false,
                  //       data: true
                  //     },	// Let's negotiate data channels as well
									// 		// If you want to test simulcasting (Chrome and Firefox only), then
									// 		// pass a ?simulcast=true when opening this demo page: it will turn
									// 		// the following 'simulcast' property to pass to janus.js to true
									// 		simulcast: doSimulcast,
									// 		success: function(jsep) {
                  //
                  //
                  //       console.log('deviceList::', deviceList);
                  //
                  //       Janus.debug("Got SDP!");
									// 			Janus.debug('Janus.debug:::::', jsep);
									// 			echotest.send({"message": body, "jsep": jsep});
									// 		},
									// 		error: function(error) {
									// 			Janus.error("WebRTC error:", error);
									// 		}
									// 	});

                    restartCapture(devices[1].deviceId);


                },
                error: function(cause) {
                        // Couldn't attach to the plugin
                        console.log("error:::", cause);
                },
                consentDialog: function(on) {
                        // e.g., Darken the screen if on=true (getUserMedia incoming), restore it otherwise
                },
                onmessage: function(msg, jsep) {
                        // We got a message/event (msg) from the plugin
                        // If jsep is not null, this involves a WebRTC negotiation
                        echotest.handleRemoteJsep({jsep: jsep});
                },
                onlocalstream: function(stream) {
                        // We have a local stream (getUserMedia worked!) to display
                        console.log('onlocalstream:::', stream);



                        Janus.debug(" ::: Got a local stream :::");
      									Janus.debug(stream);
                        this.showVideo = true;
                        // if($('#myvideo').length === 0) {
      									// 	$('#videos').removeClass('hide').show();
      									// 	$('#videoleft').append('<video class="rounded centered" id="myvideo" width=320 height=240 autoplay muted="muted"/>');
      									// }

                        //Janus.attachMediaStream($('#myvideo').get(0), stream);

                        Janus.attachMediaStream(document.getElementById('myvideo'), stream);

      									document.getElementById('myvideo').setAttribute('muted', "muted");

      									// if(echotest.webrtcStuff.pc.iceConnectionState !== "completed" &&
      									// 		echotest.webrtcStuff.pc.iceConnectionState !== "connected") {
                        //
      									// 	$("#videoleft").parent().block({
      									// 		message: '<b>Publishing...</b>',
      									// 		css: {
      									// 			border: 'none',
      									// 			backgroundColor: 'transparent',
      									// 			color: 'white'
      									// 		}
      									// 	});
                        //
                        //
      									// 	// No remote video yet
      									// 	$('#videoright').append('<video class="rounded centered" id="waitingvideo" width=320 height=240 />');
      									// 	if(spinner == null) {
      									// 		var target = document.getElementById('videoright');
      									// 		spinner = new Spinner({top:100}).spin(target);
      									// 	} else {
      									// 		spinner.spin();
      									// 	}
      									// }



      									var videoTracks = stream.getVideoTracks();
      									// if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
      									// 	// No webcam
      									// 	$('#myvideo').hide();
      									// 	if($('#videoleft .no-video-container').length === 0) {
      									// 		$('#videoleft').append(
      									// 			'<div class="no-video-container">' +
      									// 				'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
      									// 				'<span class="no-video-text">No webcam available</span>' +
      									// 			'</div>');
      									// 	}
      									// } else {
      									// 	$('#videoleft .no-video-container').remove();
      									// 	$('#myvideo').removeClass('hide').show();
      									// }



                },
                onremotestream: function(stream) {
                        // We have a remote stream (working PeerConnection!) to display


                },
                oncleanup: function() {
                        // PeerConnection with the plugin closed, clean the UI
                        // The plugin handle is still valid so we can create a new one
                },
                detached: function() {
                        // Connection with the plugin closed, get rid of its features
                        // The plugin handle is not valid anymore
                }
        });
      },
      error: function(cause) {
              // Error, can't go on...
              alert('error');
      },
      destroyed: function() {
              // I should get rid of this
              alert('destroyed');
      }
    });
  }

  ngOnInit() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        console.log('stream::::', stream);
      })
      .catch(function(err) {
        /* handle the error */
      });

    this.configureJanus()
  }





}
