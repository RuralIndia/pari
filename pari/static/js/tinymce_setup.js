function tinyMCEInit(selector) {
    var imgContainerClass = 'image-container',
        imgContainerImgSelector = '.' + imgContainerClass + '>img';

    tinymce.init({
        selector: selector || ".mceEditor",
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
                width: 900,
                height: 500,
                resizable: "yes",
                scrollbars: "yes",
                inline: "yes",
                close_previous: "no",
                buttons:[{
                    text: 'Cancel',
                    onclick: 'close'
                }]
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
            "template paste"
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

            alignleft: [
                {selector: 'figure,p,h1,h2,h3,h4,h5,h6,td,th,tr,div,ul,ol,li', styles: {textAlign: 'left'}, defaultBlock: 'div'},
                {selector: imgContainerImgSelector, collapsed: false, styles: {'display': 'table', 'float': 'left'},
                    onformat: function(elm, fmt) {
                        tinymce.activeEditor.dom.setStyles(elm.parentNode, fmt['styles']);
                    }
                },
                {selector: 'img,table', collapsed: false, styles: {'float': 'left'}}
            ],

            aligncenter: [
                {selector: 'figure,p,h1,h2,h3,h4,h5,h6,td,th,tr,div,ul,ol,li', styles: {textAlign: 'center'}, defaultBlock: 'div'},
                {selector: imgContainerImgSelector, collapsed: false, styles: {'display': 'table', float: '', 'margin-left': 'auto', 'margin-right': 'auto'},
                    onformat: function(elm, fmt) {
                            tinymce.activeEditor.dom.setStyles(elm.parentNode, fmt['styles']);
                    }
                },
                {selector: 'img', collapsed: false, styles: {display: 'block', marginLeft: 'auto', marginRight: 'auto'}},
                {selector: 'table', collapsed: false, styles: {marginLeft: 'auto', marginRight: 'auto'}}
            ],

            alignright: [
                {selector: 'figure,p,h1,h2,h3,h4,h5,h6,td,th,tr,div,ul,ol,li', styles: {textAlign: 'right'}, defaultBlock: 'div'},
                {selector: imgContainerImgSelector, collapsed: false, styles: {'display': 'table', 'float': 'right'},
                    onformat: function(elm, fmt) {
                        tinymce.activeEditor.dom.setStyles(elm.parentNode, fmt['styles']);
                    }
                },
                {selector: 'img,table', collapsed: false, styles: {'float': 'right'}}
            ]

        },

        setup: function (ed) {
            ed.addButton('dropcaps', {
                text: 'Drop Caps',
                icon: false,
                onclick: function () {
                    ed.formatter.apply('dropcaps');
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

            ed.addButton('caption', {
                text: 'Caption',
                icon: false,
                onclick: function () {
                    var element = ed.selection.getNode(),
                        parent = element.parentElement,
                        currentCaption = parent.getAttribute('data-label');

                    ed.windowManager.open({
                        title: currentCaption ? 'Edit Caption' : 'Add Caption',
                        body: [
                            {type: 'textbox', name: 'caption', label: 'Caption', value: currentCaption}
                        ],
                        onsubmit: function (e) {
                            var updatedCaption = e.data.caption;

                            if(parent.className === imgContainerClass){
                                parent.setAttribute('data-label', updatedCaption);
                                return;
                            }

                            var dom = ed.dom;
                            var container = dom.create('a', {'class': imgContainerClass,
                                'data-label': updatedCaption,
                                'href': '',
                                'style': element.getAttribute('style')});
                            element.setAttribute('style', '');
                            dom.insertAfter(container, element);
                            container.appendChild(element);

                            var containerWrapper = dom.create('span', {'class': 'image-container-wrapper' });
                            dom.insertAfter(containerWrapper, container);
                            containerWrapper.appendChild(container);
                        }
                    });
                }
            });

        }
    });
}
tinyMCEInit();
