        var monthName = new Array(
                'Gen',
                'Feb',
                'Mar',
                'Apr',
                'Mag',
                'Giu',
                'Lug',
                'Ago',
                'Set',
                'Ott',
                'Nov',
                'Dic');
        var hourap = new Array(12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);
        function showTime(){
            var dateObj = new Date();
            var day = dateObj.getDate(), month = dateObj.getMonth(), year = dateObj.getFullYear(), hour = dateObj.getHours(), minutes = (dateObj.getMinutes()<=9?'0'+dateObj.getMinutes():dateObj.getMinutes());
            var string  = monthName[month]+
            ' '+day+
            ', '+year+
            '<br />'+hourap[hour]+
            ':'+minutes+
            ' '+(hour<=11?'am':'pm');
            var timeDiv = document.getElementById('orario');
            if(timeDiv !== null) {
                timeDiv.innerHTML = string;
                timeDiv.setAttribute('datetime',year+'-'+(month+1<=9?'0'+(month+1):month+1)+'-'+day+' '+hour+':'+minutes);

            };
        };
setInterval(showTime,1000);

        function aggiungiOra(){
            var dateObj = new Date();
            var hour = dateObj.getHours() + 2;
            var minute = (dateObj.getMinutes()<=9?'0'+dateObj.getMinutes():dateObj.getMinutes());
            var boxOrario = document.getElementById('oraScadenza');
            if (boxOrario != null ) {
                boxOrario.innerHTML = string;
                boxOrario.value = hour+":"+minute;
            }

        };

setInterval(aggiungiOra,1000)
