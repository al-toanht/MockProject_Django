$(document).ready(function() {
  const citySelect = $('#city');
  const feeShippingDisplay = $('#feeShippingDisplay');
  const feeShippingInput = $('#feeShippingInput');
  const totalPriceDisplay = $('#totalPriceDisplay');
  const totalPriceInput = $('#totalPriceInput');
  const subPrice = $('#subPrice');

  function updatePrices() {
    const feeShipping = parseFloat(citySelect.find('option:selected').data('fee')) || 0;
    const formattedFeeShipping = feeShipping.toFixed(1);
    const formattedTotalPrice = (parseFloat(subPrice.val()) + feeShipping).toFixed(1);

    feeShippingDisplay.text(`$${formattedFeeShipping}`);
    feeShippingInput.val(formattedFeeShipping);
    totalPriceDisplay.text(`$${formattedTotalPrice}`);
    totalPriceInput.val(formattedTotalPrice);
  }

  updatePrices();

  $("#city").change(function(e) {
    updatePrices();
  });

  $("#addToOrder").click(function(e){
    e.preventDefault();
    var email = $('input[name=email]').val();
    var phone_number = $('input[name=phone_number]').val();
    var shipping_address = $('input[name=shipping_address]').val();
    var city = $('#city').val();
    var productId =  $('input[name=productId]').val();
    var quantity =  $('input[name=quantity]').val();
    var price =  $('input[name=price]').val();
    var totalPrice =  $('input[name=totalPrice]').val();
    var payment_method = $('input[name=payment_method]:checked').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
      method: 'POST',
      url: "/check-out",
      dataType: "JSON",
      data: {
          'email': email,
          'phone_number' : phone_number,
          'shipping_address': shipping_address,
          'city': city,
          'productId': productId,
          'quantity' : quantity,
          'price': price,
          'totalPrice': totalPrice,
          'payment_method': payment_method,
          csrfmiddlewaretoken: token
      },
      success: function(response) {
      
        Swal.fire({
            title: response.message,
            icon: 'success',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'OK'
          }).then((result) => {
            if (result.isConfirmed) {
              location.reload();
            }
        });
      },
      error: function (response) {
        $('.error-message').remove();
        var fieldStatus = {};
        if ('errors' in response.responseJSON) {
          for (var fieldName in response.responseJSON.errors) {
            var errorMessage = response.responseJSON.errors[fieldName];
            fieldStatus[fieldName] = true
            $('#errors').after('<div class="error-message">' + errorMessage + '</div>');
            if (fieldName != '') {
              $('#' + fieldName).addClass('error');
            }
          }
        }

        $('input').not('[name=csrfmiddlewaretoken]').each(function() {
        var fieldName = $(this).attr('name');
          if (!fieldStatus[fieldName]) {
            $('#' + fieldName).removeClass('error');
        }
        });
      }
    });
  });
});