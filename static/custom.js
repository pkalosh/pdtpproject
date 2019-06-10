$(function () {

  $(".js-media-account").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });


   $(".js-media-twitter").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('.ajax-loader').css("visibility", "visible");
      },
      success: function (data) {
        $('.ajax-loader').css("visibility", "hidden");
        $("#modal-book").modal("show");
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-add").on("submit", ".js-account-create-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#fb-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");  // <-- Close the modal
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

  $(".js-footprint-scan").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('.ajax-loader').css("visibility", "visible");
      },
      success: function (data) {
        $('.ajax-loader').css("visibility", "hidden");
        $("#modal-book").modal("show");
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });


  $(".js-footprint-display").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('.ajax-loader').css("visibility", "visible");
      },
      success: function (data) {
        $('.ajax-loader').css("visibility", "hidden");
        $("#modal-book").modal("show");
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });


  $(".add-phone-number").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-add").on("submit", ".add-phone-submit", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#phone-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");  // <-- Close the modal
          notify('success','Phone number Added Successfully');
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });


  $(".add-email").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-add").on("submit", ".add-email-submit", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#email-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");
          notify('success','Email Added Successfully');  // <-- Close the modal
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });


  $(".js-additional-info").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });

  $(".js-additional-info-update").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-add").on("submit", ".js-additional-info-submit", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#additional-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");  // <-- Close the modal
          notify('success','Details Added Successfully');
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

  $("#modal-add").on("submit", ".js-additional-info-update", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#additional-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");  // <-- Close the modal
          notify('success','Details Added Successfully');
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });


  $(".js-additional-info-delete").click(function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add").modal("show");
      },
      success: function (data) {
        $("#modal-add .modal-content").html(data.html_form);
      }
    });
  });
  $("#modal-add").on("submit", ".js-info-delete-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#additional-table tbody").html(data.html_book_list);  // <-- Replace the table body
          $("#modal-add").modal("hide");  // <-- Close the modal
          notify('success','Details Deleted Successfully');
        }
        else {
          $("#modal-add .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });
});