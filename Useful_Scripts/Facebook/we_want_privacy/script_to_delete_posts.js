# run on:
# https://www.facebook.com/your-username/allactivity?privacy_source=activity_log&log_filter=cluster_11

$("html, body").animate({ scrollTop: $(document).height() }, "slow");
setInterval (function () {
  var last = $("._6a._6b.uiPopover.rfloat a span").last().click();
  $("span:contains(Delete):visible").click();
  setTimeout(function () {
    $("button:contains(Delete Post):visible").click();
    last.closest("table").remove();
  }, 1000);
}, 7000);