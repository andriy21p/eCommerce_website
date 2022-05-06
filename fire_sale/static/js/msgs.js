
acceptAnOffer = function() {
    let offerId = $("#offerId").val();
    //let offerAmount = $("#offerAmount").val();
    //let bidder = $("#bidder").val();
    //let seller = $("#seller").val();
    console.log("OfferId is: ", offerId)
    // $("#itemPlaceAnOffer").prop("disabled", true);
    // send the bid to the server
    //let formData = {offer: offerId, amount: offerAmount, bidder: bidder, seller: seller};
    //$.ajax({
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
    //});
}

proceedToCheckout = function() {

}