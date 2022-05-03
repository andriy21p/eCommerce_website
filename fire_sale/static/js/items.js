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
                return '<div class="col-sm-12 col-md-6 col-lg-3 col-xxl-2 text-center bg-white border rounded p-2">\n' +
                       '    <img class="productImage rounded" src="'+d.image+'" alt="'+d.image_description+'" />\n' +
                       '    <p style="text-overflow: ellipsis;overflow:hidden;white-space:nowrap;">'+d.name+'</p>\n' +
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