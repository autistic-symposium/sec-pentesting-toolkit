# run on your account
var i = setInterval(function () {
  $ul = $("#wmMasterViewThreadlist")
  if (!$ul.find("li").length) return clearInterval(i);
  $ul.find("li").last().find("span").click()
  $("button:contains('Actions')").click()
  $("span:contains('Delete Conversation...')").click()
  $("input[value='Delete Conversation']").click()
}, 500);