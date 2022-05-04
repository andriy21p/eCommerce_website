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
                       '       <small>' + d.category + '</small></div><br/>\n'+
                       '    <div class="img-hover-zoom">'+
                       '    <img class="productImage rounded shadow" src="'+d.image+'" alt="'+d.image_description+'" />' +
                       '    </div>\n' +
                       '    <p class="singleItemName">'+d.name+'</p><p class="singleItemPrice">'+d.price_minimum.toLocaleString()+'</p>\n' +
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