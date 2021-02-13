$(function () {
  $("#lnch_btn").on("click", function () {
    setTimeout(function () {
      $("#lnch").addClass("launching").text("SENDING");
      $("#lnch_btn").addClass("launching");
    }, 0);
  });
});