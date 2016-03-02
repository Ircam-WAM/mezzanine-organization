/**
 * Plugins
 */
var gulp         = require('gulp');
    sass         = require('gulp-sass'),
    postcss      = require('gulp-postcss'),
    autoprefixer = require('autoprefixer'),
    mqpacker     = require('css-mqpacker'),
    plumber      = require('gulp-plumber'),
    concat       = require('gulp-concat'),
    notify       = require("gulp-notify"),
    uglify       = require('gulp-uglify');



/**
 * Paths
 */
var scssSrc = 'app/festival/static/scss/',
    jsSrc   = 'app/festival/static/js/',
    cssDist = 'app/festival/static/css/',
    cssDjango = 'data/static/css/';




/**
 * Environnement
 */

env = (function() {
    var env = 'development';
    return env;
} ());

// Set to production (for builds)
gulp.task( 'envProduction', function() {
    env = 'production';
});


/**
 * CSS
 */
gulp.task('css', function () {

    if ( env === 'production' ) {
        output = 'compressed';
    } else {
        output = 'expanded';
    }

    var processors = [
        autoprefixer({browsers: ['last 2 version']}),
        mqpacker({
            sort: true
        })
    ];

    return gulp.src( scssSrc + 'index.scss'  )
        .pipe(sass({
            outputStyle : output,
            sourceComments: 'normal'
        })
        .on('error', notify.onError("Error: <%= error.message %>")))
        .pipe(postcss(processors))
        .pipe(gulp.dest(cssDist))
        .pipe(gulp.dest(cssDist));

});

/**
 * JAVASCRIPT
 */

// Concatenate all JS libs
gulp.task('jsLibs', function() {
    console.log(jsSrc);
    return gulp.src(jsSrc + 'plugins/*.js')
    .pipe(concat('plugins.js'))
    .pipe(gulp.dest(jsSrc));
});

// Move main js script file
// gulp.task('jsScripts', function() {
//   gulp.src(jsSrc + 'index.js')
//     .pipe(plumber())
//     .pipe(gulp.dest(dist + 'js/'));
// });

// Move and minify main js script file
// gulp.task('jsScriptsBuild', function() {
//   gulp.src('src/js/index.js')
//     .pipe(plumber())
//     .pipe(uglify())
//     .pipe(gulp.dest(dist + 'js/'));
// });


 /**
 * TASKS
 */

// default task (development)
gulp.task('default', ['css', 'jsLibs'], function () {
    gulp.watch( scssSrc + '/**/*.scss', ['css']);
    gulp.watch( jsSrc + 'plugins/*.js', ['jsLibs']);
});

// Build tasks
gulp.task( "build", [ 'envProduction', 'css', 'jsScriptsBuild'], function () {
    console.log("Build complete !");
});