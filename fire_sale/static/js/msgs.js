
acceptAnOffer = function() {
    let msgId = $("#msgId").val();
    let accepted = true;
    //let offerAmount = $("#offerAmount").val();
    //let bidder = $("#bidder").val();
    //let seller = $("#seller").val();
    console.log("msgId is: ", msgId)
    // $("#itemPlaceAnOffer").prop("disabled", true);
    // send the bid to the server
    let formData = {offer: msgId, accepted: accepted};
    $.ajax({
    //    url: '/checkout/' + offerId,
    //    type: 'POST',
    //    headers: { "X-CSRFToken": getCookie("csrftoken") },
    //    data: formData,
    //    success: function (response) {
            // Needs to refresh messages

    //    },
    //    error: function (xhr, status, error) {
            // add toaster with error
    //        console.error(error);
    //    }
    });
}

proceedToCheckout = function() {

}