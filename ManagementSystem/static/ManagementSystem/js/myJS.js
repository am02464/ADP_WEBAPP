$(document).ready(function() {
        $('#id_class_selector').change(function(){
            var data;
            $.ajax({
                type: 'post',
                data: {
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
                    'class_selector':$('#id_class_selector').val(),
                    'batch_selector':$('#id_batch_selector').val(),

                },
                success: function (data) {
                       $('#student-table').html(data)
                }
            });
       });

       $('#id_batch_selector').change(function(){
           var data;
            $.ajax({
                type: 'post',
                data: {
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
                    'class_selector':$('#id_class_selector').val(),
                    'batch_selector':$('#id_batch_selector').val(),

                },
                success: function (data) {
                       $('#student-table').html(data)
                }
            });
       });


       // class script
       $(document).on('submit','#generic-class',function(e){
            e.preventDefault();
            $.ajax({
                type: 'post',

                data: {
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),

                    'name': $('#id_name').val(),
                    'section':$('#id_section').val(),
                    'begindate_month':$('#id_begindate_month').val(),
                    'enddate_month': $('#id_enddate_month').val(),
                    'begindate_day':$('#id_begindate_day').val(),
                    'enddate_day': $('#id_enddate_day').val(),
                    'begindate_year':$('#id_begindate_year').val(),
                    'enddate_year': $('#id_enddate_year').val(),
                    },
                success: function (data) {
                    $("#generic-class").html(data)

                }
            });
       });


        $(document).on('submit','#student-form',function(e){
            e.preventDefault();
            $.ajax({
                type: 'post',
                data: {
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
                    'firstname' :$('#id_firstname').val(),
                    'lastname'   :$('#id_lastname').val(),
                    'fathername' :$('#id_fathername').val(),
                    'fatherscnic' :$('#id_fatherscnic').val(),
                    'studentscnic' :$('#id_studentscnic').val(),
                    'fathersnumber' :$('#id_fathersnumber').val(),
                    'studentsnumber' :$('#id_studentsnumber').val(),
                    'batch' :$('#id_batch').val(),
                    },
                success: function (data) {
                    $("#student-form").html(data)

                }
            });
       });
});

