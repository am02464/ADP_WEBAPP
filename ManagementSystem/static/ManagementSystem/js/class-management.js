var classInformationUpdate = function () {
    /*
        Binds when class information is updated
    */
    $('#update-class').click(function (event) {
        $('#loader').css('diplay', 'normal', 'visibility', 'visible');
        event.preventDefault();
        fields = $('#view-class-modal #generic-form .field');
        var dict = {};
        i = 0;
        while (i < fields.length) {
            dict[fields[i].name] = fields[i].value;
            i++;
        }
        dict['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();
        $.post($(this).attr("href"), dict, function (data) {
            $('#view-class-modal #generic-form').html(data);
            $('#loader').css('visibility', 'hidden');
        });

    });

}
classInformationUpdate();


var bindWithClassLinks = function () {
    /**

      Binds With Class Links....

    **/

    $('.class-link').click(function (event) {
        //bool = true;
        event.preventDefault();
        var href = $(this).attr('href');
        $.get($(this).attr('href'), function (data) {
            $('#view-class-modal .modal-body').html(data);
            $('#update-class').attr('href', href);
            //other add here
            classInformationUpdate();
        });
    });
}

bindWithClassLinks();


var updateClassTable = function () {
    /*
      Updates class-table
    */
    $.get("{% url 'update_classes' %}", function (data) {
        $("#class-table").html(data);
        bindWithClassLinks();
    });
}

updateClassTable();



$('#add-class').click(function (event) {
    $('#loader').css('diplay', 'normal', 'visibility', 'visible');
    event.preventDefault();
    fields = $('#add-class-modal #generic-form .field');
    console.log(fields);
    var dict = {};
    i = 0;
    while (i < fields.length) {
        dict[fields[i].name] = fields[i].value;
        i++;
    }
    dict['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();
    console.log(dict);

    $.post($(this).attr("href"), dict, function (data) {
        $('#add-class-modal #generic-form').html(data);
        updateClassTable();
        bindWithForm();
        validationStyles();
        $('#loader').css('visibility', 'hidden');
    });

});
