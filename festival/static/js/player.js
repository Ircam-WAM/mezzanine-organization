
function init_player(){
    var audio;
    var playlist;
    var tracks;
    var current;

    current = 0;
    audio = $('#audio');
    playlist = $('#playlist');
    tracks = playlist.find('li a');
    len = tracks.length - 1;
    audio[0].volume = .90;
//    audio[0].play();
    playlist.find('a').click(function(e){
        e.preventDefault();
        link = $(this);
        current = link.parent().index();
        run_player(link, audio[0]);
    });
    audio[0].addEventListener('ended',function(e){
        current++;
        if(current == len){
            current = 0;
            link = playlist.find('a')[0];
        }else{
            link = playlist.find('a')[current];
        }
        run_player($(link),audio[0]);
    });
}
function run_player(link, player){
    $(player).find('#primarysrc').attr('src', link.attr('href'));
    $(player).find('#secondarysrc').attr('src', link.attr('data-altsrc'));
    par = link.parent();
    par.addClass('active').siblings().removeClass('active');
    player.load();
    player.play();
}

init_player();
