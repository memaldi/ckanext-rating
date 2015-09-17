$("#rating-widget").bind('rated', function (event, value) {
  var packageId = $("#package-id")[0].value;
  $.post("/api/3/action/rating_create", JSON.stringify({"package": packageId, "rating": value}), 'json')
});
