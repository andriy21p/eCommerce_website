categoryFilter = function(category) {
    let workingHeader = '<H1>Items refreshing ...</H1>';
    $('#items-header').html($.parseHTML(workingHeader));
    $.ajax({
        url: '/item/?category=' + category,
        type: 'GET',
        success: function(response) {
            let newHeader = '<H1>Items</H1>';
            if (category != '') {
                newHeader += ' in category ' + category + ' - <a href="#" onclick="categoryFilter(\'\')">clear category filter</a>';
            }
            let newHtml = response.items.map(d => {
                return '<div class="singleItemWidth text-center bg-white border border-success rounded p-2 align-items-stretch flex-grow-2 m-1">\n' +
                       '<div class="border border-info rounded bg-light"' +
                       '     onclick="categoryFilter(\'' + d.category + '\');">' +
                       '       <i class="' + d.category_icon + '"></i>'+
                       '       <small>' + d.category + '</small></div><br/>\n' +
                       '    <span onclick="getItemDetails(' + d.id + ');" data-bs-toggle="modal" data-bs-target="#itemDetailModal">' +
                       '     <div class="img-hover-zoom">'+
                       '      <img class="itemImage rounded shadow" src="'+d.image+'" alt="'+d.image_description+'" />' +
                       '     </div>\n' +
                       '     <p class="singleItemName">'+d.name+'</p><p class="singleItemPrice">'+d.price_minimum.toLocaleString("is-IS")+'</p>\n' +
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
    $('#itemDetailModalLabel').text('') ;
    $('#itemDetailModalBody').text('fetching, just a moment ...') ;
    $('.carousel-inner').html('') ;
    $("#itemDetailCategoryTag").removeClass();
    $.ajax({
        url: '/item/' + id,
        type: 'GET',
        success: function(response) {
            if (response.items.length > 0) {
                let item = response.items[0] ;
                $('#itemDetailModalLabel').text(item.name) ;
                $('#itemDetailModalBody').text(item.description) ;
                $('#itemDetailCategoryTag').addClass(item.category_icon) ;
                $('#itemDetailCategoryName').text(item.category) ;
                $('#itemDetailModalCondition').text('Condition: '+item.condition) ;
                for (let i = 0 ; i < item.images.length ; i++) {
                    let newHtml = '<div class="carousel-item" id="carousel-item">\n' +
                                  '  <img class="d-block w-auto itemDetailImage" src="' + item.images[i].url + '" alt="' + item.images[i].description + '">\n' +
                                  '</div>\n'
                    console.log($.parseHTML(newHtml));
                    $('.carousel-inner').append($.parseHTML(newHtml));
                }
                $('.carousel-item').first().addClass('active');
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