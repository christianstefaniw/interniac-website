$(function () {
  $("#lnch_btn").on("click", function () {
    setTimeout(function () {
      $("#lnch").addClass("launching").text("SENDING");
      $("#lnch_btn").addClass("launching");
    }, 0);

    setTimeout(function () {
      $("#lnch").addClass("launched").text("SENT");
      $("#lnch_btn").addClass("launched");
    }, 1500);
  });
});