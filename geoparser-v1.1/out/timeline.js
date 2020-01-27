// timeline.js - Javascript for timeline visualisation interface.

var tl;
 function onLoad(docDate, eventsList, tlBox, wdthmonth, wdthyear) {
   var eventSource = new Timeline.DefaultEventSource();
   var bandInfos = [
     Timeline.createBandInfo({
         eventSource:    eventSource,
         date:           docDate,
         width:          wdthmonth, 
         intervalUnit:   Timeline.DateTime.MONTH, 
         intervalPixels: 150
     }),
     Timeline.createBandInfo({
         overview:       true,
         eventSource:    eventSource,
         date:           docDate,
         width:          wdthyear, 
         intervalUnit:   Timeline.DateTime.YEAR, 
         intervalPixels: 200
     })
   ];
   bandInfos[1].syncWith = 0;
   bandInfos[1].highlight = true;
   tl = Timeline.create(document.getElementById(tlBox), bandInfos);
   // either load from XML file or pass events info as JSON object defined in calling html page
   Timeline.loadXML(eventsList, function(xml, url) { eventSource.loadXML(xml, url); })
//   eventSource.loadJSON(eventsList,"");
 }


var resizeTimerID = null;
 function onResize() {
     if (resizeTimerID == null) {
         resizeTimerID = window.setTimeout(function() {
             resizeTimerID = null;
             tl.layout();
         }, 500);
     }
 }