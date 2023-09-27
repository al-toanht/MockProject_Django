$(document).ready(function() {
  $(".remove-from-cart").click(function(event) {
    event.preventDefault(); 
    var cartItemId = $(this).data("cart-id");
    var removeUrl = $(this).data('remove-url');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        type: "POST",
        url: removeUrl,
        data: {
            'cart_item_id': cartItemId,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(response) {
            if (response.success) {
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
            }
        },
        error: function(response) {   
          if (response.responseJSON.error === 'Cart item not found') {
            Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Item not found in the cart',
              footer: '<a href="#">Need help?</a>'
            })   
          }
          if (response.responseJSON.error === 'Not authenticated') {
            window.location.replace(window.location.protocol + "/" + "login");
          }
        }
    });
  });
  
  $(".numeric-input").on("input", function() {
    // Xóa tất cả các ký tự không phải số và bắt đầu bằng 0
    $(this).val($(this).val().replace(/[^0-9]/g, "").replace(/^0+/g, ""));
  });

  $(".quantity-input").on("input", function(){
      var idProduct = $(this).attr('data-url');
      var quantity = parseInt($(this).val());
      var price = $("#discount_price"+idProduct).val();
      if (!isNaN(quantity) && quantity > 0) {
        var totalProduct = price*quantity
        $("#quantity"+idProduct).val(quantity)
        $("#priceLabel"+idProduct).text('₫'+totalProduct.toFixed(1))
        $("#price"+idProduct).val(totalProduct.toFixed(1))
        calculateTotalPrice();
      } else {
        $("#quantity"+idProduct).val("")
      }
  });

    $(".decrease-quantity").click(function(event){
      event.preventDefault(); 
      var idProduct = $(this).attr('data-url');
      var quantity = $("#quantity"+idProduct).val();
      var price = $("#discount_price"+idProduct).val();
      if (quantity != 1) {
        --quantity
        var totalProduct = price*quantity
        $("#quantity"+idProduct).val(quantity)
        $("#priceLabel"+idProduct).text('₫'+totalProduct.toFixed(1))
        $("#price"+idProduct).val(totalProduct.toFixed(1))
        calculateTotalPrice();
      }
    });
    $(".increase-quantity").click(function(event){
      event.preventDefault(); 
      var idProduct = $(this).attr('data-url');
      var quantity = $("#quantity"+idProduct).val();
      var price = $("#discount_price"+idProduct).val();
        ++quantity
        var totalProduct = price*quantity
        $("#quantity"+idProduct).val(quantity)
        $("#priceLabel"+idProduct).text('₫'+totalProduct.toFixed(1))
        $("#price"+idProduct).val(totalProduct.toFixed(1))
        calculateTotalPrice();
    });

    var numProduct = document.querySelectorAll('input[type="checkbox"][data-url]')
    var count = 0
    $('input[type="checkbox"]').on("click", function(event){
        var idProduct = $(this).attr('data-url')
        if (idProduct !== undefined) {
          if ($(this).is(':checked')) {
            $('#labelCheck'+idProduct).attr("class", "stardust-checkbox stardust-checkbox--checked")
            ++count
          } else {
            $('#labelCheck'+idProduct).attr("class", "stardust-checkbox");
            --count
          }
          if (count == numProduct.length) {
            $('input[name="checkAll"]').prop('checked', true)
            $(".stardust-checkbox").attr("class", "stardust-checkbox stardust-checkbox--checked");
          }
          if (count < numProduct.length) {
            $('input[name="checkAll"]').prop('checked', false)
            $('label[name="checkAll"]').attr("class", "stardust-checkbox");
          }
        } else {
          if ($(this).is(':checked')) {
            $('input[type="checkbox"]').prop('checked', true)
            $(".stardust-checkbox").attr("class", "stardust-checkbox stardust-checkbox--checked");
            count = numProduct.length
          } else {
            $('input[type="checkbox"]').prop('checked', false)
            $(".stardust-checkbox").attr("class", "stardust-checkbox");
            count = 0
          }
        }
        calculateTotalPrice();
        $('#numProduct').text(`Tổng thanh toán (${count} Sản phẩm):`)
    });

    $("#buttonAll").click(function(event){
      event.preventDefault(); 
      if ($('input[type="checkbox"][name="checkAll"]').is(':checked')) {
        $('input[type="checkbox"]').prop('checked', false)
        $(".stardust-checkbox").attr("class", "stardust-checkbox");
        count = 0
      } else {
        $('input[type="checkbox"]').prop('checked', true)
        $(".stardust-checkbox").attr("class", "stardust-checkbox stardust-checkbox--checked");
        count = numProduct.length
      }
      calculateTotalPrice();
      $('#numProduct').text(`Tổng thanh toán (${count} Sản phẩm):`)
    });
});


function calculateTotalPrice() {
  var totalPrice = 0
  //loop through subtotal
  $('.totalPrice').each(function() {

    var id = $(this).attr('data-url')
    if ($("#cart"+id).is(':checked')) {
      var value = $(this).val() != "" ? parseFloat($(this).val()) : 0;
      totalPrice += value;
    }
  })

  if (totalPrice > 0) {
    $('#totalPrice').text(`₫${totalPrice.toFixed(1)}`)
    $('input[name="totalPrice"]').val(totalPrice.toFixed(1));
  } else {
    $('#totalPrice').text('₫0')
  }
}