
function acceptAnOffer(msgId) {
    let is_true = false;
    if (document.getElementsByClassName(".offerAccept") === true){
        let is_true = true;
    }
    //let msgId = $("#msgId").val();
    let accept = true;
    console.log("msgId is: ", msgId, "Class: ", is_true)
    // $("#itemPlaceAnOffer").prop("disabled", true);
    // send the bid to the server
     let formData = {id: msgId};
    $.ajax({
        url: "/message/" + msgId + "/accept",
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: formData,
        success: function (response) {
            // Needs to refresh messages

        },
        error: function (xhr, status, error) {
            // add toaster with error
    //        console.error(error);
        }
    });
}

proceedToCheckout = function() {

}