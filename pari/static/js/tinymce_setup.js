if (typeof tinyMCE != 'undefined') {
    tinymce.init({
        selector: ".mceEditor",
        remove_script_host: false,
        convert_urls: false,
        relative_urls: false,
        height: 400,
        paste_as_text: true,
        font_formats: "Merriweather=merriweather;" +
                "Open Sans=Open Sans;"+
                "Andale Mono=andale mono,times;"+
                "Arial=arial,helvetica,sans-serif;"+
                "Arial Black=arial black,avant garde;"+
                "Book Antiqua=book antiqua,palatino;"+
                "Comic Sans MS=comic sans ms,sans-serif;"+
                "Courier New=courier new,courier;"+
                "Georgia=georgia,palatino;"+
                "Helvetica=helvetica;"+
                "Impact=impact,chicago;"+
                "Symbol=symbol;"+
                "Tahoma=tahoma,arial,helvetica,sans-serif;"+
                "Terminal=terminal,monaco;"+
                "Times New Roman=times new roman,times;"+
                "Trebuchet MS=trebuchet ms,geneva;"+
                "Verdana=verdana,geneva;"+
                "Webdings=webdings;"+
                "Wingdings=wingdings,zapf dingbats",
        fontsize_formats: "8pt 9pt 10pt 11pt 12pt 12.5pt 14pt 16pt 18pt 24pt 36pt",
        file_browser_callback: function (field_name, url, type, win) {
            var frame = tinyMCE.activeEditor.windowManager.open({
                file: window.__filebrowser_url + '?pop=2&type=' + type,
                width: 820,
                height: 500,
                resizable: "yes",
                scrollbars: "yes",
                inline: "yes",
                close_previous: "no"
            }, {
                window: win,
                input: field_name,
                editor_id: tinyMCE.editors[0].id
            });

            window.tinymce_activeEditor = tinyMCE.activeEditor;
            window.tinymce_activeFrame = frame;
            window.tinymce_activeInput = field_name;
            return false;
        },

        theme: "modern",
        plugins: [
            "advlist autolink lists link image charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime media nonbreaking save table contextmenu directionality",
            "template paste caption"
        ],
        content_css: "/static/css/tinymce.css",

        toolbar1: "insertfile undo redo | styleselect | bold italic lineheight dropcaps blockquote | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image caption",
        toolbar2: "fullscreen print preview media | fontsizeselect forecolor backcolor fontselect",
        image_advtab: true,
        templates: [
            {title: 'Test template 1', content: 'Test 1'},
            {title: 'Test template 2', content: 'Test 2'}
        ],
        formats: {
            dropcaps: {inline: 'span', classes: "dropcaps"},
            lineheight: {block: 'p', styles: {'lineHeight': '%value'}},
            blockquote: {block: 'blockquote', classes: "blockquote"}
        },

        setup: function (ed) {
            ed.addButton('dropcaps', {
                text: 'Drop Caps',
                icon: false,
                onclick: function () {
                    ed.formatter.apply('dropcaps');
                }
            });
            ed.addButton('blockquote', {
                text: 'Blockquote',
                icon: false,
                onclick: function () {
                    ed.formatter.apply('blockquote');
                }
            });
            ed.addButton('lineheight', {
                text: 'Line height',
                icon: false,
                onclick: function () {
                    ed.windowManager.open({
                        title: 'Specify line height',
                        body: [
                            {type: 'textbox', name: 'lineheight', label: 'Value'}
                        ],
                        onsubmit: function (e) {
                            ed.formatter.apply('lineheight', {value: e.data.lineheight});
                        }
                    });
                }
            });
        }
    });

}