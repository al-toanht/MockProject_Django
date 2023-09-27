$(document).ready(function() {
    $('input[name=quantity]').keydown(function(e) {
    var key = e.charCode || e.keyCode || 0;
          return (
              key == 8 || 
              key == 9 ||
              key == 13 ||
              key == 46 ||
              key == 110 ||
              key == 190 ||
              (key >= 35 && key <= 40) ||
              (key >= 48 && key <= 57) ||
              (key >= 96 && key <= 105));
    });

    $(".addToCart").click(function(e){
      e.preventDefault();
      var product_id = $('input[name=product_id]').val();
      var quantity = $('input[name=quantity]').val();
      var color = $('input[name=color]:checked').val();
      var token = $('input[name=csrfmiddlewaretoken]').val()
      var size = $('input[name=size]:checked').val();
        $.ajax({
          method: 'POST',
          url: "/add-to-cart",
          dataType: "JSON",
          data: {
              'product_id': product_id,
              'quantity' : quantity,
              'size': size,
              'color': color,
              csrfmiddlewaretoken: token
          },
          success: function(response) {
            $("#error").html("").removeClass("text-danger");
            $("#divColorSize").removeClass("detail-danger");
            Swal.fire({
              title: response.message,
              icon: 'success',
              confirmButtonColor: '#3085d6',
              confirmButtonText: 'OK'
            }).then((result) => {
              if (result.isConfirmed) {
                location.reload()
              }
            })
          },
          error: function(response) {   
            if (response.responseJSON.error !== 'Not Login') {
              $("#error").html(response.responseJSON.error).addClass("text-danger");
              $("#divColorSize").addClass("detail-danger");
            }
            if (response.responseJSON.error === 'Not Login') {
              window.location.replace(window.location.protocol + "/" + "login");
            }
          }      
        });
    });

    $(".decrease-quantity").click(function(e){
      var quantity = $("#quantity").val();
      if (quantity != 1) {
        $("#quantity").val(--quantity)
      }
    });
    $(".increase-quantity").click(function(e){
      var quantity = $("#quantity").val();
      $("#quantity").val(++quantity)
    });
});
  