(function(global, $) {

  "use strict";

  /**
   * Helper for displaying spinner based on query string and loading time.
   * Set query string "?spinner=false" to prevent showing a spinner for this request.
   * Set query string "?tolerance={time in miliseconds}" to set the tolerance for a specific request.
   * @param {oject} Set options param:
   *   tolerance -> Define max loading time in miliseconds before the spinner is shown for all requests.
   */
  function ajaxLoadingIndicator(options) {

    options = $.extend({
      tolerance: 300
    }, options || {});

    var spinner = $("#ajax-spinner");

    var requests = {};

    var getParameterByName = function(name, url) {
      name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
      var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
      var results = regex.exec(url);
      return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    };

    var hasSpinner = function(url) {
      var spinnerFlag = getParameterByName("spinner", url);
      if(spinnerFlag === "" && spinnerFlag !== "false") {
        return true;
      }
      return false;
    };

    var trackRequest = function(url) {
      if(hasSpinner(url)) {
        var tolerance = getParameterByName("tolerance", url);
        tolerance = tolerance === "" ? options.tolerance : tolerance;
        var timeout = global.setTimeout(function() { spinner.show(); }, tolerance);
        requests[url] = timeout;
      }
    };

    var untrackRequest = function(url) {
      global.clearTimeout(requests[url]);
      delete requests[url];
      spinner.hide();
    };

    $(document).off("ajaxStart");
    $(document).on("ajaxSend", function(event, jqxhr, params) { trackRequest(params.url); });
    $(document).on("ajaxComplete", function(event, jqxhr, params) { untrackRequest(params.url); });
  }

  $(document).ready(function() { ajaxLoadingIndicator(); });


}(window, jQuery));
