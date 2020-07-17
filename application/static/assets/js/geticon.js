$( document ).ready(function() {
    $("#icons").select2({
    placeholder: "Select an option",
    allowClear: true,
    escapeMarkup: function (m) {
        return m;
    },
    });

    function add(value) {
    var newOption = new Option(value, value, false, false);
    $("#icons").append(newOption).trigger("change");
    }

    load_state("icons");
    function load_state(id, parent_id) {
    var html_code = "";
    var location = getURL();
    $.getJSON(location, function (data) {
        $.each(data, function (key, value) {
        add(value.icon);
        });
    });
    }
});