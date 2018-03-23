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

    /* initialize the calendar
     -----------------------------------------------------------------*/
    //Date for the calendar events (dummy data)
    var date = new Date()
    var d    = date.getDate(),
        m    = date.getMonth(),
        y    = date.getFullYear()

    

    $('#calendar').fullCalendar({
      header    : {
        left  : 'prev, next, today',
         center: 'title',
        right : 'month'
      },
      buttonText: {
        today: 'today',
        month: 'month',
        // week : 'week',
        // day  : 'day'
      },
      //Random default events
      events    : "/bible_study/calendar/",
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
  
        var my_start = $.fullCalendar.moment(date.format());
        copiedEventObject.start           = my_start

        // var my_end = $.fullCalendar.moment(date.format()+'T'+copiedEventObject.end_tm);
        // copiedEventObject.end           = my_end

        //copiedEventObject.textColor           = originalEventObject.textColor
        copiedEventObject.backgroundColor = originalEventObject.backgroundColor
        copiedEventObject.borderColor =  originalEventObject.borderColor
        copiedEventObject.title =  originalEventObject.title


        //copiedEventObject.allDay          = allDay    
        // render the event on the calendar if ajax save was successful
         $.ajax({
                        type: 'POST',
                        url: "/bible_study/calendar/",
                        data:{
                            action : "ADD",
                            date : date.format(),   
                            event_type : copiedEventObject.event_type,
                            event_type_id : copiedEventObject.event_type_id,
                            scripture : copiedEventObject.scripture,
                            note   : copiedEventObject.note,
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
                        url: "/bible_study/calendar/",
                        data:{
                            id: event.id,
                            action: 'DELETE'
                        },
                        success:function(data){
                          
                          if (data.success == 'true' ) {

                                var str = "<div class='external-event bg-red'>"
                                var el = $( str ).appendTo( '#external-events' ).text( event.title );        

                                el.data('eventObject', {
                                  id   : -99, 
                                  title :  event.title, 
                                  scripture  : event.scripture,
                                  event_type  : event.event_type,
                                  event_type_id  : event.event_type_id,
                                  note : event.note,
                                  backgroundColor : event.backgroundColor,
                                  borderColor : event.borderColor,
                                  textColor : event.textColor
                                });

                                el.draggable({
                                   zIndex        : 1070,
                                   revert        : true, // will cause the event to go back to its
                                   revertDuration: 0  //  original position after the drag
                                   });

                                // $(function () {
                                //   $('[data-toggle="tooltip"]').tooltip()
                                // }) 

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
             
             $.ajax({
                        type: 'POST',
                        url: "/bible_study/calendar/",
                        data:{
                            action : "UPDATE",
                            id: event.id,
                            date : event.start.format()
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
        eventRender: function(event, element) {


              if (event.day_type === "HOLIDAY")
                $(element).tooltip({title: "Public Holiday" });             
              else if (event.day_type === "BIRTHDAY")
                $(element).tooltip({title: "Happy birthday!" });             
              else
              {

                 if (event.scripture)
                 {
                    var title = event.scripture + " " + event.note 
                 }
                else
                  {
                    var title = event.note;
                  }
                  
                  // element.popover({
                  //   title: title,
                  //   placement: event.start.getHours()>12?'top':'bottom',
                  //   content: event.event_type + " " + title
                  //   });

                  $(element).tooltip({title:  title  }); 
              }
        },
        eventDataTransform: function(eventData){

          if (eventData.day_type === "HOLIDAY" || eventData.day_type === "BIRTHDAY" )
            // || perms.accounts.is_bible_study_admin )
            eventData.editable = false;

          return eventData;
        
        },
    }) // Calendar

    /* ADDING EVENTS */

    $('#add-new-event').click(function (e) {
      e.preventDefault()
      //Get value and make sure it is not null

      var event_type = $('#event_type :selected').text()
      if (event_type.length == 0) {
        return
      }

      var event_type_id = $('#event_type').val()

      var scripture = $('#scripture').val()
      
      var note = $('#note').val()

      if (note.length == 0) {
        return
      }
      //Create events


      // christiaan '#00a65a'
      // sara '#f39c12'
     var mColor = '';
     
     var titleToolTip =  note;

      if (event_type == 'SWS' || event_type == 'SWS Campus') {
               mColor = '#00a65a';
               var str = "<div class='external-event bg-green' >"
               var el = $( str ).appendTo( '#external-events' ).text( event_type + " " + scripture );
      }
      else {
               mColor = '#f39c12';
               var str = "<div class='external-event bg-yellow' >"
               var el = $( str ).appendTo( '#external-events' ).text( event_type + " " + scripture );
      }

       el.data('eventObject', 
              {id   : -99, 
              title :  event_type,
              scripture  :  scripture,
              event_type  : event_type,
              event_type_id  : event_type_id,
              note : note,
              backgroundColor : 'white',
              borderColor : 'white',
              textColor : mColor
        });

        el.draggable({
                   zIndex        : 1070,
                   revert        : true, // will cause the event to go back to its
                   revertDuration: 0  //  original position after the drag
                   });
      
      // $(function () {
      //     $('[data-toggle="tooltip"]').tooltip()
      // })

      //Remove event from text input
      $('#note').val('')

    }); /* ADDING EVENTS */
}) /* document */