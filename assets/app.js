// Click-to-load YouTube (privacy: nothing loads from YouTube until the patient taps play)
document.addEventListener('click', function (e) {
  var btn = e.target.closest('.frame[data-yt]');
  if (!btn) return;
  var id = btn.getAttribute('data-yt');
  var f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
  f.title = btn.getAttribute('aria-label') || 'Exercise video';
  f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
  f.allowFullscreen = true;
  btn.replaceWith(f);
});

// If YouTube thumbnails are blocked (some hospital/guest networks), hide the broken
// image and leave the play button on the dark panel — the video still opens on tap.
document.addEventListener('error', function (e) {
  if (e.target.matches && e.target.matches('.video img')) e.target.style.display = 'none';
}, true);
