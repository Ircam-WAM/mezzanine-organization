import videojs from 'video.js';
import playlistMaker from './playlist-maker';

/**
 * The video.js playlist plugin. Invokes the playlist-maker to create a
 * playlist function on the specific player.
 *
 * @param {Array} list
 */
const plugin = function(list, item) {
  playlistMaker(this, list, item);
};

videojs.plugin('playlist', plugin);

export default plugin;
