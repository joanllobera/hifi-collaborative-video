import { Component, OnInit } from '@angular/core';
import { RecordService } from  '../record.service';
import { Observable } from  'rxjs/Observable';
import { Observer } from 'rxjs';


declare var Janus: any;

@Component({
  selector: 'app-camera-back',
  templateUrl: './camera-back.component.html',
  styleUrls: ['./camera-back.component.css']
})
export class CameraBackComponent implements OnInit {

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

    var server = 'https://192.168.10.252:8080/janus',;

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
      	// Negotiate WebRTC
      	var body = { "audio": true, "video": true };
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
					// No "iceServers" is provided, meaning janus.js will use a default STUN server
					// Here are some examples of how an iceServers field may look like to support TURN
					// 		iceServers: [{url: "turn:yourturnserver.com:3478", username: "janususer", credential: "januspwd"}],
					// 		iceServers: [{url: "turn:yourturnserver.com:443?transport=tcp", username: "janususer", credential: "januspwd"}],
					// 		iceServers: [{url: "turns:yourturnserver.com:443?transport=tcp", username: "janususer", credential: "januspwd"}],
					// Should the Janus API require authentication, you can specify either the API secret or user token here too
					//		token: "mytoken",
					//	or
					//		apisecret: "serversecret",
					success: function() {
						// Attach to echo test plugin
						janus.attach(
							{
								plugin: "janus.plugin.echotest",
								opaqueId: opaqueId,
								success: function(pluginHandle) {
									$('#details').remove();
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
								},
								error: function(error) {
									console.error("  -- Error attaching plugin...", error);
								},
								consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");
									// if(on) {
									// 	// Darken screen and show hint
									// 	$.blockUI({
									// 		message: '<div><img src="up_arrow.png"/></div>',
									// 		css: {
									// 			border: 'none',
									// 			padding: '15px',
									// 			backgroundColor: 'transparent',
									// 			color: '#aaa',
									// 			top: '10px',
									// 			left: (navigator.mozGetUserMedia ? '-100px' : '300px')
									// 		} });
									// } else {
									// 	// Restore screen
									// 	$.unblockUI();
									// }
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
									// if($('#myvideo').length === 0) {
									// 	$('#videos').removeClass('hide').show();
									// 	$('#videoleft').append('<video class="rounded centered" id="myvideo" width=320 height=240 autoplay muted="muted"/>');
									// }
                  Janus.attachMediaStream(document.getElementById('myvideo'), stream);

                  document.getElementById('myvideo').setAttribute('muted', "muted");





								},
								onremotestream: function(stream) {
									Janus.debug(" ::: Got a remote stream :::");
									Janus.debug(stream);
									// var addButtons = false;
									// if($('#peervideo').length === 0) {
									// 	addButtons = true;
									// 	$('#videos').removeClass('hide').show();
									// 	$('#videoright').append('<video class="rounded centered hide" id="peervideo" width=320 height=240 autoplay/>');
									// 	// Show the video, hide the spinner and show the resolution when we get a playing event
									// 	$("#peervideo").bind("playing", function () {
									// 		$('#waitingvideo').remove();
									// 		if(this.videoWidth)
									// 			$('#peervideo').removeClass('hide').show();
									// 		if(spinner !== null && spinner !== undefined)
									// 			spinner.stop();
									// 		spinner = null;
									// 		var width = this.videoWidth;
									// 		var height = this.videoHeight;
									// 		$('#curres').removeClass('hide').text(width+'x'+height).show();
									// 	});
									// }
									// Janus.attachMediaStream($('#peervideo').get(0), stream);
									// var videoTracks = stream.getVideoTracks();
									// if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
									// 	// No remote video
									// 	$('#peervideo').hide();
									// 	if($('#videoright .no-video-container').length === 0) {
									// 		$('#videoright').append(
									// 			'<div class="no-video-container">' +
									// 				'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
									// 				'<span class="no-video-text">No remote video available</span>' +
									// 			'</div>');
									// 	}
									// } else {
									// 	$('#videoright .no-video-container').remove();
									// 	$('#peervideo').removeClass('hide').show();
									// }
									// if(!addButtons)
									// 	return;
									// // Enable audio/video buttons and bitrate limiter
									// audioenabled = true;
									// videoenabled = true;
									// $('#toggleaudio').removeAttr('disabled').click(
									// 	function() {
									// 		audioenabled = !audioenabled;
									// 		if(audioenabled)
									// 			$('#toggleaudio').html("Disable audio").removeClass("btn-success").addClass("btn-danger");
									// 		else
									// 			$('#toggleaudio').html("Enable audio").removeClass("btn-danger").addClass("btn-success");
									// 		echotest.send({"message": { "audio": audioenabled }});
									// 	});
									// $('#togglevideo').removeAttr('disabled').click(
									// 	function() {
									// 		videoenabled = !videoenabled;
									// 		if(videoenabled)
									// 			$('#togglevideo').html("Disable video").removeClass("btn-success").addClass("btn-danger");
									// 		else
									// 			$('#togglevideo').html("Enable video").removeClass("btn-danger").addClass("btn-success");
									// 		echotest.send({"message": { "video": videoenabled }});
									// 	});
									// $('#toggleaudio').parent().removeClass('hide').show();
									// $('#bitrate a').removeAttr('disabled').click(function() {
									// 	var id = $(this).attr("id");
									// 	var bitrate = parseInt(id)*1000;
									// 	if(bitrate === 0) {
									// 		Janus.log("Not limiting bandwidth via REMB");
									// 	} else {
									// 		Janus.log("Capping bandwidth to " + bitrate + " via REMB");
									// 	}
									// 	$('#bitrateset').html($(this).html() + '<span class="caret"></span>').parent().removeClass('open');
									// 	echotest.send({"message": { "bitrate": bitrate }});
									// 	return false;
									// });
									// if(Janus.webRTCAdapter.browserDetails.browser === "chrome" || Janus.webRTCAdapter.browserDetails.browser === "firefox" ||
									// 		Janus.webRTCAdapter.browserDetails.browser === "safari") {
									// 	$('#curbitrate').removeClass('hide').show();
									// 	bitrateTimer = setInterval(function() {
									// 		// Display updated bitrate, if supported
									// 		var bitrate = echotest.getBitrate();
									// 		//~ Janus.debug("Current bitrate is " + echotest.getBitrate());
									// 		$('#curbitrate').text(bitrate);
									// 		// Check if the resolution changed too
									// 		var width = $("#peervideo").get(0).videoWidth;
									// 		var height = $("#peervideo").get(0).videoHeight;
									// 		if(width > 0 && height > 0)
									// 			$('#curres').removeClass('hide').text(width+'x'+height).show();
									// 	}, 1000);
									// }
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
					}
				});

	}});
  }

  ngOnInit() {
    // navigator.mediaDevices.getUserMedia({ video: true })
    //   .then(function(stream) {
    //     console.log('stream::::', stream);
    //   })
    //   .catch(function(err) {
    //   });
    this.configureJanus()
  }




}
