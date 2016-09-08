var Audio = function() {

    //
    // Init
    //
    this.init();

    this.audios = [];
    this.playlists = [];

};

Audio.prototype.init = function() {

    var that = this,
        as, i, playlist;

    audiojs.events.ready(function() {

        as = audiojs.createAll();

        for(i = 0; i<as.length; i++) {

            playlist = $(as[i].element).parent().next('.audio-playlist');

            //
            // Future refs
            //
            that.audios.push(as[i]);
            that.playlists.push(playlist[0]);

            //
            // Set the trackEnded function
            //
            as[i].settings.trackEnded = function() {

                var idx, next, playlist;

                idx = that.audios.indexOf(this);
                playlist = that.playlists[idx];

                var next = playlist.find('li.playing').next();
                if (!next.length) next = playlist.find('li').first();
                next.addClass('playing').siblings().removeClass('playing');
                this.load($('a', next).attr('data-src'));
                this.play();

            };

            //
            // Load the first audio
            //
            var first = playlist.find('li a').attr('data-src');
            playlist.find('li').first().addClass('playing');
            as[i].load(first);

            playlist.find('li').bind('click', function(e) {

                var idx = that.playlists.indexOf($(this).parent().get(0));

                e.preventDefault();
                $(this).addClass('playing').siblings().removeClass('playing');
                that.audios[idx].load($('a', this).attr('data-src'));
                that.audios[idx].play();

            });

        }

    });

};

module.exports = Audio;
