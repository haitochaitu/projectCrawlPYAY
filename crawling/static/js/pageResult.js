$(document).ready(function(){
   crawled_list = []
   url = $('#id_seed_url').val()
   depth = $('#id_traverse_depth').val();
   urls_counter = 0;
   $(':input[type="submit"]').prop('disabled', true);
   go_for_crawl(url,depth)
   function go_for_crawl(url, depth) {
      formData = {};
      formData['url'] = url
      formData['depth'] = depth
      var promise = $.ajax({
          url:'/crawlfromurlapi/',
          type:'post',
          dataTye: 'json',
          contentType:"application/json; charset=utf-8",
          async:true,
          data:JSON.stringify(formData),
          beforeSend: function() {
            $("#loader").css("display", "block");
            urls_counter++;
          },
          complete: function() {
            urls_counter--;
            if(urls_counter <= 0) {
               $("#loader").css("display", "none");
               $(':input[type="submit"]').prop('disabled', false);
            }
          },
          success: function(response){
             $(function () {
                 crawled_list.push(url)
                  $('<tr>').append(
                  $('<td>').text(url.slice(0,100))).appendTo('#id_crawled_table');
                  var img = "<span>"
                  $.each(response["image"], function (i, item) {
                       if(item != "No Images") {
                          img = img + "<img src='"+item+ "' alt='Invalid Image' height='100' width='100'>";}
                       else { img = item }
                  })
                  img += "</span>"
                  $('<tr>').append(
                  $('<td>').html(img)).appendTo('#id_crawled_table');
                  if (depth > 0){
                      depth -= 1
                      $.each(response["url"], function (i, url) {
                           if($.inArray(url, crawled_list) == -1) {
                              go_for_crawl(url,depth)
                            }
                      });
                  }
             });
          },
          error:function(response){
             alert("Error: " + response.responseText)
             $("input[id=submit_single_form]").attr("disabled", false);
             $("input[id=submit_single_form]").attr("value", "Submit");
             $("input[id=submit_multiple_form]").attr("disabled", false);
          }
      })
   }
});


