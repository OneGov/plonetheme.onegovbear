/*
TinyMCE Dialog is loaded in an iFrame so it's not possible
to override the stlying. So this script copies the related
stylings to the head section of the iframe.
TODO: Not working on page load.
 */

(function($, global) {

  "use strict";

  $(function() {

    var css = $('link[href*="/theming.css"]').clone();

    var insertCSS = function() {
      if (global.tinyMCE && global.tinyMCE.editors) {
        $.each(global.tinyMCE.editors, function(idx, editor) {
          if (editor.windowManager && editor.windowManager.onOpen) {
            editor.windowManager.onOpen.add(function() {
              if (this.lastId) {
                /*
                  _add is not in scope of Event.
                  so best guess is to bind the _add function to add.
                 */
                global.tinymce.dom.Event._add = global.tinymce.dom.Event.add;
                $("#" + this.lastId.replace("wrapper", "ifr")).contents().find("head").append(css);
                $(".mceLeft").hide();
              }
            });
            editor.windowManager.onClose.add(function() {
              $(".mceLeft").show();
            });
          }
        });
      }
    };

    insertCSS();

    $(document).on("onLoad", insertCSS );
  });

}(jQuery, window));

