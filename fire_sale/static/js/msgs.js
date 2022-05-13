function init_messages() {
    const modal = new bootstrap.Modal(document.getElementById("modalDiv"));

    htmx.on("htmx:afterSwap", (e) => {
        // Response targeting #dialog => show the modal
        if (e.detail.target.id == "dialog") {
            modal.show()
        }
    })

    htmx.on("htmx:beforeSwap", (e) => {
        // Empty response targeting #dialog => hide the modal
        if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide()
        e.detail.shouldSwap = false
        }
    })

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = ""
    })
};

function acceptAnOffer(msgId) {
    let is_true = false;
    let btn = $('.offerAccept').addClass('disabled') ;
    //let msgId = $("#msgId").val();
    let accept = true;
    // console.log("msgId is: ", msgId, "Class: ", is_true)
    // $("#itemPlaceAnOffer").prop("disabled", true);
    // send the bid to the server
     let formData = {id: msgId};
    $.ajax({
        url: "/message/" + msgId + "/accept",
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: formData,
        success: function (response) {
            $(btn).text('Offer accepted, buyer sent to checkout');
        },
        error: function (xhr, status, error) {
            // add toaster with error
            console.error(error);
        }
    });
}
