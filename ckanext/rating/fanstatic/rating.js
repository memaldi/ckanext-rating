$(".rateit").bind('rated', function (event, value) {
  var eventID = event.currentTarget.id;
  var packageID = eventID.replace("rating-widget-", "");
  $.post("/api/3/action/rating_create", JSON.stringify({"package": packageID, "rating": value}), 'json')
});

/*$("#rating-widget").bind('rated', function (event, value) {
  console.log(event);
  var packageId = $("#package-id")[0].value;
  $.post("/api/3/action/rating_create", JSON.stringify({"package": packageId, "rating": value}), 'json')
});*/
