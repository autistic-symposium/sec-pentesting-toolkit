# run on:
#https://www.facebook.com/your-username/allactivity?privacy_source=activity_log&log_filter=likes

$("html, body").animate({ scrollTop: $(document).height() }, "slow");
setInterval(function () {
  var last = $("._6a._6b.uiPopover.rfloat a span").last().click();
  $("span:contains(Unlike):visible").click();
  var post = last.closest("[data-ft]");
  post.prev().remove();
  post.remove();
}, 400);