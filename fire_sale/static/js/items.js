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
            return decodeURI(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

loading = function(showIndicator) {
    if (showIndicator) {
        $('#index-loading').show();
        $('#index-sort-order').hide();
    } else {
        $('#index-loading').hide();
        $('#index-sort-order').show();
    }
}

formatTags = function(tags) {
    res = '';
    if (tags.length>0) {
        for (let i=0 ; i < tags.length-1 ; i++) {
            res += tags[i].name +', ';
        }
        res += tags[tags.length-1].name;
    }
    return 'Tags for this item: ' + res;
}

formatItem = function(d, withCategoryFilter, withDataDismiss) {
    res = '<div class="singleItemItem singleItemWidth text-center bg-white border border-success rounded p-2 align-items-stretch flex-grow-2 m-1">\n' +
          '<span class="d-none" id="sort_order_item">' + JSON.stringify(d.sort) + '</span>\n' +
          '<span class="d-none" id="tags_item">' + JSON.stringify(d.tags) + '</span>\n' +
          '<div class="border border-info rounded bg-light" data-toggle="tooltip" title="' + formatTags(d.tags) + '"' ;
    if (withCategoryFilter) {
        res +='     onclick="categoryFilter(\'' + d.category + '\', ' + d.category_id + ');"';
    }
    res+= '>' +
          '       <i class="' + d.category_icon + '"></i>'+
          '       <small>' + d.category + '</small></div><br/>\n' +
          '    <span onclick="getItemDetails(' + d.id + ');"' ;
    if (withDataDismiss) {
        res +=' data-bs-dismiss="modal"';
    }
    res+= '>    <div class="img-hover-zoom">'+
          '      <img class="itemImage rounded shadow" src="'+d.images[0].url+'" alt="'+safe(d.images[0].description)+'" />' +
          '     </div>\n' +
          '     <p class="singleItemName">'+safe(d.name)+'</p><p class="singleItemPrice">'+d.price_minimum.toLocaleString("is-IS")+'</p>\n' +
          '    </span>' +
          '</div>';

    return res ;
}

let tagCloud = [];

updateTagCloud = function(tags) {
    if (tagCloud.length == 0) {
        $('#tagFilter').empty() ;
    }
    if (tags.length > 0) {
        for (let i=0 ; i < tags.length ; i++) {
            let inCloud = tagCloud.indexOf(tags[i].name);
            // console.log(tags[i].name+':'+inCloud);
            if (inCloud<0) {
                tagCloud.push(tags[i].name);  // save that this tag has been added

                newHtml = '<div class="text-center bg-opacity-75 bg-info bg-gradient border border-secondary rounded p-2 align-items-stretch flex-grow-2 m-1" onclick="tagFilterBy(' + tags[i].id + ')">' +
                    '<span class="d-none" id="tagId">' + tags[i].id + '</span>' +
                    '<span>' + tags[i].name + '</span>' +
                    '</div>';
                $('#tagFilter').append(newHtml);
            }
        }
    }
    if (tagCloud.length > 0) {
        $('#tag-filter-block').show();
    }
}

tagFilterBy = function(id) {
    $('.singleItemItem').hide();
    $('.singleItemItem').each(function(idx, e) {
        let tags_element = e.firstElementChild.nextElementSibling.textContent.replaceAll('\'', '"');
        let tags = JSON.parse(tags_element);
        for (let i=0 ; i < tags.length ; i++) {
            if (tags[i].id == id) {
                $(e).show();
            }
        }
    });
}

clearFilterTags = function() {
    $('.singleItemItem').show();
    $('#tag-filter-block').hide();
}


categoryFilter = function(category, categoryId) {
    loading(true);
    let workingHeader = '<H1>Items refreshing ...</H1>';
    $('.categoryFilterItems').removeClass('active')
    $('#items-header').html($.parseHTML(workingHeader));
    tagCloud = [];
    $.ajax({
        url: '/item/?category=' + category,
        type: 'GET',
        success: function(response) {
            // console.log($('.category_' + categoryId));
            $('.category_' + categoryId).addClass('active')
            let newHeader = '';
            if (category != '') {
                newHeader += ' Items in category ' + category + ' - <a href="#" onclick="categoryFilter(\'\')">clear category filter</a>';
            }
            let newHtml = response.items.map(d => {
                // setum inn tóma mynd ef það er engin mynd til að koma í veg fyrir villur
                if (d.images.length == 0) { let images = {url: '', description: ''} ; d.images.push(images);}
                updateTagCloud(d.tags);
                return formatItem(d, true, false);
            });
            $('#items-container').html(newHtml.join(''));
            $('#items-header').html($.parseHTML(newHeader));
            loading(false);

        },
        error: function(xhr, status, error) {
            // add toaster with error
            console.error(error);
            loading(false);
        }
    })
}

getSimilarItems = function(id) {
    $('#similar-items-container').empty();
    $.ajax({
        url: '/item/' + id + '/similar',
        type: 'GET',
        success: function (response) {
            if (response.items.length > 0) {
                $('#similar-items-header').show();
                let newHtml = response.items.map(d => {
                    // setum inn tóma mynd ef það er engin mynd til að koma í veg fyrir villur
                    if (d.images.length == 0) { let images = {url: '', description: ''} ; d.images.push(images);}
                return formatItem(d, false, true);
                });
                $('#similar-items-container').append(newHtml);
            }
        },
        error: function(xhr, status, error) {
            // add toaster with error
            console.error(error);
        }
    });
}

getItemDetails = function(id) {
    let myModal = new bootstrap.Modal(document.getElementById('itemDetailModal'), {});
    myModal.show()

    $('#itemPlaceAnOffer').prop('disabled', true);
    $('#itemDetailModalLabel').text('') ;
    $('#itemDetailModalCurrentResult').text('') ;
    $('#itemDetailModalBody').html('<div id="index-loading" class="spinner-border text-success" role="status">\n' +
        '<span class="visually-hidden">Loading...</span></div>') ;
    $('.carousel-inner').html('') ;
    $('#itemDetailCategoryTag').removeClass();
    $('.itemDetailBidding').hide();
    $('#similar-items-container').empty();
    $('#similar-items-header').hide();

    $.ajax({
        url: '/item/' + id,
        type: 'GET',
        success: function(response) {
            if (response.items.length > 0) {
                getSimilarItems(id);
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

                if (item.seller != item.current_user && item.current_highest_bidder != item.current_user) {
                    // allow user to make an offer
                    $('.itemDetailBidding').show();
                    $('#itemPlaceAnOffer').prop('disabled', false);
                    $('#placeBid').attr('placeholder', 'Type an amount, for example ' + (item.current_price + Math.round(item.current_price / 10)));
                    $('#placeBid').val('');
                    $('#itemId').val(id);
                    if (item.number_of_bids > 2) {
                        // console.log(item.number_of_bids);
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

changeSortOrder = function() {
    let new_order = $('#sort_order').val();
    document.cookie = 'sortorder=' + new_order;
    // location.reload();

    // loop though all items on display and change the flex-box ordering element for the new sort order
    $('.singleItemItem').each(function(i, flex_item) {
        let ordering = flex_item.firstElementChild.textContent.replaceAll('\'', '"');
        let obj = JSON.parse(ordering);
        let new_ord = '0'
        switch(new_order) {
            case '0': new_ord=obj.popa ; break ;
            case '1': new_ord=obj.popd ; break ;
            case '2': new_ord=obj.pricea ; break ;
            case '3': new_ord=obj.priced ; break ;
            case '4': new_ord=obj.alpha ; break ;
            case '5': new_ord=obj.alphd ; break ;
        }
        $(flex_item).css('order', new_ord);
        // console.log($(flex_item).css('order'));
    })
}

$(document).ready(function(){
    loading(false);
    if (!window.location.search.includes('search=') && window.location.href.includes('/item/')) {
        categoryFilter('');
    }
    function get_badge() {
        $.get('/message/number_of_unread', function (data, textStatus, jqXHR) {
            let number = data.number_of_unread_messages;
            if (number > 0) {
                $('.messageNotifierNumber').text(number);
                $('.messageNotifier').fadeIn();
                if (data.show_toast) {
                    alert('NEW MESSAGE HAS ARRIVED FROM '+data.latest_from);
                }
            } else {
                $('.messageNotifier').fadeOut();
            }
        }).fail( function(error) {
            // unable to get messages badge, lets hide it for now
            $('.messageNotifier').fadeOut();
        });
    };
    $('#tag-filter-block').hide();
    get_badge();
    setInterval(get_badge,20000);
    sorder = getCookie('sortorder') ;
    // console.log(sorder);
    if (sorder != undefined) {
        $('#sort_order').val(sorder);
    }
});
