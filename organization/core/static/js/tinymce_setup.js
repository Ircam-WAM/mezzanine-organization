function custom_file_browser(field_name, url, type, win) {
    return tinyMCE.activeEditor.windowManager.open({
        title: "Select " + type + " to insert",
        file: window.__filebrowser_url + "?pop=5&type=" + type,
        width: 800,
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "yes",
        close_previous: "no"
    }, {
        window: win,
        input: field_name
    }), !1
}
var language_codes = {
    ar: "ar",
    ca: "ca",
    cs: "cs",
    da: "da",
    de: "de",
    es: "es",
    et: "et",
    fa: "fa",
    "fa-ir": "fa_IR",
    fi: "fi",
    fr: "fr_FR",
    "hr-hr": "hr",
    hu: "hu_HU",
    "id-id": "id",
    "is-is": "is_IS",
    it: "it",
    ja: "ja",
    ko: "ko_KR",
    lv: "lv",
    nb: "nb_NO",
    nl: "nl",
    pl: "pl",
    "pt-br": "pt_BR",
    "pt-pt": "pt_PT",
    ru: "ru",
    sk: "sk",
    sr: "sr",
    sv: "sv_SE",
    tr: "tr",
    uk: "uk_UA",
    vi: "vi",
    "zh-cn": "zh_CN",
    "zh-tw": "zh_TW",
    "zh-hant": "zh_TW",
    "zh-hans": "zh_CN"
};
jQuery(function($) {
    "undefined" != typeof tinyMCE && tinyMCE.init({
        selector: "textarea.mceEditor",
        height: "500px",
        language: language_codes[window.__language_code] || "en",
        plugins: ["advlist autolink lists link image charmap print preview anchor", "searchreplace visualblocks code fullscreen", "insertdatetime media table contextmenu paste"],
        link_list: window.__link_list_url,
        relative_urls: !1,
        convert_urls: !1,
        menubar: !0,
        statusbar: !1,
        toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image table | code fullscreen",
        image_advtab: !0,
        file_browser_callback: custom_file_browser,
        content_css: [window.__tinymce_css, '/static/admin/css/organization.css', '/static/css/index.min.css'] ,
        valid_elements: "*[*]",
        style_formats: [
            {
                title: 'Boutons', items: [
                    { title: 'Boutons Jaune', selector: 'a', classes: 'wys-button'},
                    { title: 'Boutons Jaune Small', selector: 'a', classes: 'wys-button-small'},
                    { title: 'Boutons Jaune XSmall', selector: 'a', classes: 'wys-button-xsmall'},
                    { title: 'Boutons Noir', selector: 'a', classes: 'wys-button-black'},
                    { title: 'Boutons Noir Small', selector: 'a', classes: 'wys-button-black-small'},
                    { title: 'Boutons Noir XSmall', selector: 'a', classes: 'wys-button-black-xsmall'},
                    { title: 'Boutons Blanc', selector: 'a', classes: 'wys-button-white'},
                    { title: 'Boutons Blanc Small', selector: 'a', classes: 'wys-button-white-small'},
                    { title: 'Boutons Blanc XSmall', selector: 'a', classes: 'wys-button-white-xsmall'},
                    { title: 'Boutons Blanc (bleu)', selector: 'a', classes: 'wys-button-white-main'},
                    { title: 'Boutons Blanc (bleu) Small', selector: 'a', classes: 'wys-button-white-main-small'},
                    { title: 'Boutons Blanc (bleu) XSmall', selector: 'a', classes: 'wys-button-white-main-xsmall'},
                    { title: 'Boutons Blanc (violet)', selector: 'a', classes: 'wys-button-white-accent'},
                    { title: 'Boutons Blanc (violet) Small', selector: 'a', classes: 'wys-button-white-accent-small'},
                    { title: 'Boutons Blanc (violet) XSmall', selector: 'a', classes: 'wys-button-white-accent-xsmall'}
                ]

            },
            {

                title: 'Paragraphs', items: [
                    { title: 'Highlighted paragraph', selector: 'p', classes: 'wys-highlighted-paragraph'},
                    { title: 'Small paragraph', selector: 'p', classes: 'wys-small-text'}
                ]

            },
            {

                title: 'Links', items: [
                    { title: 'Unstyled link', selector: 'a', classes: 'wys-unstyled-link'}
                ]

            }
        ],
        style_formats_merge: true
    })
});

//# sourceMappingURL=tinymce_setup.js.map
