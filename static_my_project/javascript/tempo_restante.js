 function startTimer(duration, display){
     var timer = duration, days, hours, minutes, seconds;
     setInterval(function () {
         seconds = timer
         days = Math.floor(seconds/(24*3600));
         seconds = seconds - days*24*3600;
         hours = Math.floor(seconds/3600);
         seconds = seconds - hours*3600;
         minutes = Math.floor(seconds/60);
         seconds = seconds - minutes*60;
         minutes = minutes < 10 ? "0" + minutes : minutes;
         seconds = seconds < 10 ? "0" + seconds : seconds;
         seconds = Math.floor(seconds);
         display.textContent=''
         if (days>0)
             display.textContent += days + "  Days: ";
         if (hours>0)
             display.textContent += hours+"  hours: ";
         if (minutes>0)
             display.textContent += minutes + "  minute";
         if (minutes<=1)
             display.textContent += " : " + seconds + " seconds";
         if (--timer <0) {
             timer =0
         }
     }, 1000);
 }
