//
// Require all the modules
//
var LangSelector = require('./modules/lang-selector');
var NavHeader = require('./modules/nav-header');
var OpenButton = require('./modules/open-button');
var CloseButton = require('./modules/close-button');
var CloseEscape = require('./modules/close-escape');
var Search = require('./modules/search');
var OverflowInit = require('./modules/overflow-init');
var StickyKitInit = require('./modules/sticky-kit-init');

//
// Init all the modules
//
window[LangSelector] = new LangSelector();
window[NavHeader] = new NavHeader();
window[OpenButton] = new OpenButton();
window[CloseButton] = new CloseButton();
window[CloseEscape] = new CloseEscape();
window[Search] = new Search();
window[OverflowInit] = new OverflowInit();
window[StickyKitInit] = new StickyKitInit();
