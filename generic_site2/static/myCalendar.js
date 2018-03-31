$(document).ready(function () {
 
    // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
  var csrftoken = getCookie('csrftoken');
   
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  //
  $(document).ajaxStart(function() { Pace.restart(); });

  //Timepicker
  $('.timepicker').timepicker({
      showInputs: false,
      showMeridian : false
  })


    /* initialize the external events
     -----------------------------------------------------------------*/
    function init_events(ele) {
      ele.each(function () {

        // create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
        // it doesn't need to have a start or end
        var eventObject = {
          title: $.trim($(this).text()), // use the element's text as the event title
          start_tm: "09:00:00",
          end_tm: "10:00:00"
    }

        // store the Event Object in the DOM element so we can get to it later
        $(this).data('eventObject', eventObject)

        // make the event draggable using jQuery UI
        $(this).draggable({
          zIndex        : 1070,
          revert        : true, // will cause the event to go back to its
          revertDuration: 0  //  original position after the drag
        })

      })
    }

    //init_events($('#external-events div.external-event'))

    /* initialize the calendar
     -----------------------------------------------------------------*/
    //Date for the calendar events (dummy data)
    var date = new Date()
    var d    = date.getDate(),
        m    = date.getMonth(),
        y    = date.getFullYear()
    $('#calendar').fullCalendar({
      header    : {
        left  : 'prev,next today',
        center: 'title',
        right : 'month,agendaWeek,agendaDay'
      },
      buttonText: {
        today: 'today',
        month: 'month',
        week : 'week',
        day  : 'day'
      },
      // setDefaults ( {
      //   axisFormat : "HH:mm",
      //   timeFormat : {
      //     agenda : "H:mm{ - h:mm}"
      //   },
      // minTime : 8,
      // maxTime : 24
      // }),
      slotLabelFormat : "HH:mm",
      timeFormat : 'H:mm',
      //Random default events
      events    : "/tutor/calendar/",
      editable  : true,
      droppable : true, // this allows things to be dropped onto the calendar !!!
      height    : 'auto',
      drop      : function (date, allDay) { 
    
        // this function is called when something is dropped - creates new entry in DB
                
        // retrieve the dropped element's stored Event Object
        var originalEventObject = $(this).data('eventObject')
        
        var myThis = $(this)

        // we need to copy it, so that multiple events don't have a reference to the same object
        var copiedEventObject = $.extend({}, originalEventObject)
        
        // assign it the date that was reported
  
        var my_start = $.fullCalendar.moment(date.format()+'T'+copiedEventObject.start_tm);
        copiedEventObject.start           = my_start

        var my_end = $.fullCalendar.moment(date.format()+'T'+copiedEventObject.end_tm);
        copiedEventObject.end           = my_end

 
        //copiedEventObject.allDay          = allDay    
        // render the event on the calendar if ajax save was successful
         $.ajax({
                        type: 'POST',
                        url: "/tutor/calendar/",
                        data:{
                            action : "ADD",
                            date : date.format(),        
                            start_tm : copiedEventObject.start_tm,
                            end_tm : copiedEventObject.end_tm,
                            session_type : copiedEventObject.session_type,
                            instructor_id : copiedEventObject.instructor_id,
                            student_id    : copiedEventObject.student_id,
                            session_type_id : copiedEventObject.session_type_id,
                        },
                        success:function(data){
                          
                          if (data.success == 'true') {
                              
                              copiedEventObject.id = data.event_id;
                              // the last `true` argument determines if the event "sticks" 
                              $('#calendar').fullCalendar('renderEvent', copiedEventObject, true)

                              // is the "remove after drop" checkbox checked?
                              if ($('#drop-remove').is(':checked')) {
                              // if so, remove the element from the "Draggable Events" list
                                  myThis.remove()
                              };
                          }
                          else {
                               alert("Error: Failed to add session!");
                          }
                        },
                        error: function(e){
                        alert('Error processing your request: '+e.responseText);
                        }
               });
        
      },
      eventDragStop: function( event, jsEvent, ui, view ) {
      /// deals with dragging from calendar to the external events
                
              var boxEl = jQuery('#external-events-listing');
              var ofs = boxEl.offset();

              var x1 = ofs.left;
              var x2 = ofs.left + boxEl.outerWidth(true);
              var y1 = ofs.top;
              var y2 = ofs.top + boxEl.outerHeight(true);
              
              if (jsEvent.pageX >= x1 && jsEvent.pageX<= x2 &&
                   jsEvent.pageY >= y1 && jsEvent.pageY <= y2) {
              
                  //do AJAX call if success then remove event and create new one

                  $.ajax({
                        type: 'POST',
                        url: "/tutor/calendar/",
                        data:{
                            id: event.id,
                            action: 'DELETE'
                        },
                        success:function(data){
                          
                          if (data.success == 'true' ) {

                                var titleToolTip = event.instructor + "(" + event.session_type + ")";
                                var str = "<div class='external-event bg-red'  data-toggle='tooltip' title=" + titleToolTip + ">"
                                var el = $( str ).appendTo( '#external-events' ).text( event.start_tm.slice(0,5) + " " + event.title );        

                                el.data('eventObject', {
                                  id   : -99, 
                                  title :  event.title, 
                                  start_tm :  event.start_tm.slice(0,5) + ":00", 
                                  end_tm :    event.end_tm.slice(0,5)  + ":00",
                                  instructor  : event.instructor,
                                  session_type  : event.session_type,
                                  instructor_id : event.instructor_id,
                                  student_id    : event.student_id,
                                  student    : event.student,
                                  session_type_id : event.session_type_id,
                                  backgroundColor : event.backgroundColor,
                                  borderColor : event.borderColor,
                                  textColor : event.textColor
                                });

                                el.draggable({
                                   zIndex        : 1070,
                                   revert        : true, // will cause the event to go back to its
                                   revertDuration: 0  //  original position after the drag
                                   });

                                $(function () {
                                  $('[data-toggle="tooltip"]').tooltip()
                                }) 

                                $('#calendar').fullCalendar('removeEvents', event._id);

                            }
                            else {
                                 alert("Error: Failed to remove session!");
                            }
                              
                        },
                        error: function(e){
                            alert('Error processing your request: '+e.responseText);
                        }
                 }); // ajax

                 } // if
      },
      eventDrop: function (event, delta, revertFunc) {
             
            /// we need to set event.start_tm, event.end_tm correctly
            // console.log(event.start.format());
            // console.log(event.end.format());

             $.ajax({
                        type: 'POST',
                        url: "/tutor/calendar/",
                        data:{
                            action : "UPDATE",
                            id: event.id,
                            date : event.start.format(),        
                            start_tm : event.start_tm,
                            end_tm : event.end_tm
                        },
                        success:function(data){
                          
                          if (data.success == 'true') {

                              //

                          }
                          else {
                               alert("Error: Failed to update session!");
                          }
                        },
                        error: function(e){
                        alert('Error processing your request: '+e.responseText);
                        }
               });
              
        }, // eventDrop
      eventResize: function (event, delta, revertFunc) {
             
            /// we need to set event.start_tm, event.end_tm correctly
            // console.log(event.start.format());
            // console.log(event.end.format());

             $.ajax({
                        type: 'POST',
                        url: "/tutor/calendar/",
                        data:{
                            action : "UPDATE",
                            id: event.id,
                            date : event.start.format(),        
                            start_tm : event.start_tm,
                            end_tm : event.end_tm
                        },
                        success:function(data){
                          
                          if (data.success == 'true') {

                              //

                          }
                          else {
                               alert("Error: Failed to update session!");
                          }
                        },
                        error: function(e){
                        alert('Error processing your request: '+e.responseText);
                        }
               });
              
        }, // eventResize
        eventRender: function(event, element) {
              
              if (event.day_type === "HOLIDAY")
                $(element).tooltip({title: "Public Holiday" });             
              else if (event.day_type === "BIRTHDAY")
                $(element).tooltip({title: "Happy birthday!" });             
              else
                $(element).tooltip({title: event.instructor + " (" + event.session_type + ")" }); 
        },
        eventDataTransform: function(eventData){

          if (eventData.day_type === "HOLIDAY" || eventData.day_type === "BIRTHDAY")
            eventData.editable = false;

          return eventData;
        
        },
    }) // Calendar

    /* ADDING EVENTS */

    $('#add-new-event').click(function (e) {
      e.preventDefault()
      //Get value and make sure it is not null

      
      var start_tm = $('#from-time').val()

      if (start_tm.length == 0) {
        return
      }

      start_tm = start_tm.slice(0,5)
      
      var end_tm = $('#to-time').val()

      if (end_tm.length == 0) {
        return
      }

      end_tm = end_tm.slice(0,5)

      var student = $('#student :selected').text()
      if (student.length == 0) {
        return
      }

      var student_id = $('#student').val()

      var instructor = $('#tutor :selected').text()
      if (instructor.length == 0) {
        return
      }

      var instructor_id = $('#tutor').val()

      var session_type = $('#session_type :selected').text()
      if (session_type.length == 0) {
        return
      }

      var session_type_id = $('#session_type').val()
      //Create events


      // christiaan '#00a65a'
      // sara '#f39c12'
     var mColor = '';

     var titleToolTip = instructor + "(" + session_type + ")";

      if (instructor == 'Christiaan') {
               mColor = '#00a65a';
               var str = "<div class='external-event bg-green'  data-toggle='tooltip' title=" + titleToolTip + ">"
               var el = $( str ).appendTo( '#external-events' ).text( start_tm + " "+ student );
      }
      else {
               mColor = '#f39c12';
               var str = "<div class='external-event bg-yellow'  data-toggle='tooltip' title=" + titleToolTip + ">"
               var el = $( str ).appendTo( '#external-events' ).text( start_tm + " "+ student );
      }

       el.data('eventObject', 
              {id   : -99, 
               title: student, 
               start_tm :  start_tm.slice(0,5) + ":00", 
               end_tm :    end_tm.slice(0,5)  + ":00",
               backgroundColor : 'white',
               borderColor : 'white',
               textColor : mColor,
               instructor  : instructor,
               session_type  : session_type,
               instructor_id : instructor_id,
               student_id    : student_id,
               session_type_id : session_type_id
        });

        el.draggable({
                   zIndex        : 1070,
                   revert        : true, // will cause the event to go back to its
                   revertDuration: 0  //  original position after the drag
                   });
      
      $(function () {
          $('[data-toggle="tooltip"]').tooltip()
      })

      //Remove event from text input
      $('#from-time').val('')
      $('#to-time').val('')

    }); /* ADDING EVENTS */

    /* Export Excel */

    $('#export-excel').click(function (e) {

      e.preventDefault()
      //Get value and make sure it is not null
      var start_dt = $('#calendar').fullCalendar("getView").intervalStart.format()
      var end_dt = $('#calendar').fullCalendar("getView").intervalEnd.format()
      
      console.log("click")
        $.ajax({
                        type: 'GET',
                        url: "/tutor/export/",
                        data:{
                            start : start_dt,
                            end : end_dt
                        },
                        success:function(data){
                          
                          console.log("click success before")
                          a = document.createElement('a');
                          a.href = "/tutor/export/?start=" + start_dt + "&end=" + end_dt;
                          a.click()
                          console.log("click success after")
                        
                        },
                        error: function(e){
                          alert('Error processing your request: '+e.responseText);
                        }
        });

  }); /* Export Excel */

}) /* document */