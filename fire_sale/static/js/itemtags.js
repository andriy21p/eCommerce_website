$(document).ready(function() {
   $('#id_category').change(function() {
      //get tags for currently selected category
      cat = $('#id_category').val()
      console.log(cat);
   })
});