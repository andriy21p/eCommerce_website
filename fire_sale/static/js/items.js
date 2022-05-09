safe = function(texti) {
    if (texti == undefined) {
        return '';
    } else {
        return texti.replace('<','&lt;').replace('>','&gt;');
    }
}

getCookie = function(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

categoryFilter = function(category, categoryId) {
    let workingHeader = '<H1>Items refreshing ...</H1>';
    $('.categoryFilterItems').removeClass('active')
    $('#items-header').html($.parseHTML(workingHeader));
    $.ajax({
        url: '/item/?category=' + category,
        type: 'GET',
        success: function(response) {
            console.log($('.category_' + categoryId));
            $('.category_' + categoryId).addClass('active')
            let newHeader = '<H1>Items</H1>';
            if (category != '') {
                newHeader += ' in category ' + category + ' - <a href="#" onclick="categoryFilter(\'\')">clear category filter</a>';
            }
            let newHtml = response.items.map(d => {
                // setum inn tóma mynd ef það er engin mynd til að koma í veg fyrir villur
                if (d.image.length == 0) { let image = {url: '', description: ''} ; d.image.push(image);}
                return '<div class="singleItemWidth text-center bg-white border border-success rounded p-2 align-items-stretch flex-grow-2 m-1">\n' +
                       '<div class="border border-info rounded bg-light"' +
                       '     onclick="categoryFilter(\'' + d.category + '\');">' +
                       '       <i class="' + d.category_icon + '"></i>'+
                       '       <small>' + d.category + '</small></div><br/>\n' +
                       '    <span onclick="getItemDetails(' + d.id + ');" data-bs-toggle="modal" data-bs-target="#itemDetailModal">' +
                       '     <div class="img-hover-zoom">'+
                       '      <img class="itemImage rounded shadow" src="'+d.image[0].url+'" alt="'+safe(d.image[0].description)+'" />' +
                       '     </div>\n' +
                       '     <p class="singleItemName">'+safe(d.name)+'</p><p class="singleItemPrice">'+d.price_minimum.toLocaleString("is-IS")+'</p>\n' +
                       '    </span>' +
                       '</div>'
            });
            $('#items-container').html(newHtml.join(''));
            $('#items-header').html($.parseHTML(newHeader));
        },
        error: function(xhr, status, error) {
            // add toaster with error
            console.error(error);
        }
    })
}

getItemDetails = function(id) {
    $('#itemPlaceAnOffer').prop('disabled', true);
    $('#itemDetailModalLabel').text('') ;
    $('#itemDetailModalCurrentResult').text('') ;
    $('#itemDetailModalBody').text('fetching, just a moment ...') ;
    $('.carousel-inner').html('') ;
    $('#itemDetailCategoryTag').removeClass();
    $('.itemDetailBidding').hide();
    $.ajax({
        url: '/item/' + id,
        type: 'GET',
        success: function(response) {
            if (response.items.length > 0) {
                let item = response.items[0] ;
                $('#itemDetailModalLabel').text(safe(item.name)) ;
                $('#itemDetailModalBody').text(safe(item.description)) ;
                $('#itemDetailCategoryTag').addClass(item.category_icon) ;
                $('#itemDetailCategoryName').text(item.category) ;
                $('#itemDetailModalCondition').text('Condition: '+item.condition) ;
                $('#itemDetailModalCurrentPrice').text('Current price: '+item.current_price) ;
                for (let i = 0 ; i < item.images.length ; i++) {
                    let newHtml = '<div class="carousel-item" id="carousel-item">\n' +
                                  '  <img class="d-block w-auto itemDetailImage" src="' + item.images[i].url + '" alt="' + item.images[i].description + '">\n' +
                                  '</div>\n'
                    $('.carousel-inner').append($.parseHTML(newHtml));
                }
                $('.carousel-item').first().addClass('active');

                console.log(item.seller);
                console.log(item.current_highest_bidder);
                console.log(item.current_user);
                if (item.seller != item.current_user && item.current_highest_bidder != item.current_user) {
                    // allow user to make an offer
                    $('.itemDetailBidding').show();
                    $('#itemPlaceAnOffer').prop('disabled', false);
                    $('#placeBid').attr('placeholder', 'Type an amount, for example ' + (item.current_price + Math.round(item.current_price / 10)));
                    $('#placeBid').val('');
                    $('#itemId').val(id);
                    if (item.number_of_bids > 2) {
                        console.log(item.number_of_bids);
                        $('#placeBidHelp').text('Make sure you are at least 1 higher than the current price - this item has ' + item.number_of_bids + ' bids !');
                    } else {
                        $('#placeBidHelp').text('Make sure you are at least 1 higher than the current price');
                    }
                    $('#placeBid').focus();
                } else {
                    // current user is eather the item seller, or the highest bidder
                    if (item.seller == item.current_user) {
                        $('#itemDetailModalCurrentResult').text('You are the item seller, no need to bid') ;
                    }
                    if (item.current_highest_bidder == item.current_user) {
                        $('#itemDetailModalCurrentResult').text('You are the current highest bidder, no need to bid again');
                    }
                }

            } else {
                // found nothing
            }
        },
        error: function(xhr, status, error) {
            // add toaster with error
            console.error(error);
        }
    })
}

makeAnOffer = function() {
    let id = $('#itemId').val();
    let bid = $('#placeBid').val();
    $('#itemPlaceAnOffer').prop('disabled', true);
    // send the bid to the server
    let formData = {amount: bid, item: id};
    $.ajax({
        url: '/item/' + id + '/bid',
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: formData,
        success: function (response) {
            // refresh the current view
            getItemDetails(id);
        },
        error: function (xhr, status, error) {
            // add toaster with error
            console.error(error);
            getItemDetails(id);
        }
    });
}

$(document).ready(function(){
    function get_badge() {
        $.get('/message/number_of_unread', function (data, textStatus, jqXHR) {
            let number = data.number_of_unread_messages;
            if (number > 0) {
                $('#messageNotifierNumber').text(number);
                $('.messageNotifier').show();
            } else {
                $('.messageNotifier').hide();
            }
        });
    };
    get_badge();
    setInterval(get_badge,10000);
});
