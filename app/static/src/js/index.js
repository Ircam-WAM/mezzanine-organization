//
// Require all the modules
//
var LangSelector = require('./modules/lang-selector');
var NavHeader = require('./modules/nav-header');
var OpenButton = require('./modules/open-button');
var CloseButton = require('./modules/close-button');
var CloseEscape = require('./modules/close-escape');
var Search = require('./modules/search');
var Summary = require('./modules/summary');
var OverflowInit = require('./modules/overflow-init');
var StickyKitInit = require('./modules/sticky-kit-init');
var LightSliderPageInit = require('./modules/lightsliderpage-init');
var LightSliderHomeInit = require('./modules/lightsliderhome-init');
var HomeMenu = require('./modules/home-menu');
var Audio = require('./modules/audio');

//
// Init all the modules
//
window[LangSelector] = new LangSelector();
window[NavHeader] = new NavHeader();
window[OpenButton] = new OpenButton();
window[CloseButton] = new CloseButton();
window[CloseEscape] = new CloseEscape();
window[Search] = new Search();
window[Summary] = new Summary();
window[OverflowInit] = new OverflowInit();
window[StickyKitInit] = new StickyKitInit();
window[LightSliderPageInit] = new LightSliderPageInit();
window[LightSliderHomeInit] = new LightSliderHomeInit();
window[HomeMenu] = new HomeMenu();
window[Audio] = new Audio();
