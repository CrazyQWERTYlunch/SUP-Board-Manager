$(document).ready(function () {
    var successMessage = $("#jq-notification");
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }
});