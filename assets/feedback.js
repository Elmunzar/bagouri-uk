// Feedback form. Deliberately collects no identifiers: no name, no email, no IP.
(function () {
  var form = document.getElementById('fbform');
  if (!form) return;
  var msg = document.getElementById('fbmsg');
  var ENDPOINT = form.getAttribute('data-endpoint') || 'https://feedback.bagouri.uk/submit';

  // Which guide did they come from? /feedback/?p=hip
  var p = new URLSearchParams(location.search).get('p');
  if (p && /^[a-z-]{1,40}$/.test(p)) document.getElementById('pagefield').value = p;

  // Live character counters
  form.querySelectorAll('textarea[data-count]').forEach(function (ta) {
    var out = ta.parentNode.querySelector('.count span');
    ta.addEventListener('input', function () { out.textContent = ta.value.length; });
  });

  function show(kind, text) { msg.className = 'formmsg ' + kind; msg.textContent = text; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var fd = new FormData(form);
    var body = {
      page: fd.get('page') || 'general',
      helpful: fd.get('helpful') || '',
      confusing: (fd.get('confusing') || '').trim(),
      suggestion: (fd.get('suggestion') || '').trim(),
      website: fd.get('website') || ''            // honeypot
    };
    if (!body.helpful && !body.confusing && !body.suggestion) {
      show('err', 'Please answer at least one question before sending.');
      return;
    }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Sending...';

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.querySelectorAll('fieldset').forEach(function (f) { f.remove(); });
      btn.remove();
      show('ok', 'Thank you. Your feedback has been sent, and it genuinely does change these pages.');
    }).catch(function () {
      btn.disabled = false; btn.textContent = 'Send feedback';
      show('err', 'Sorry, that did not send. Please check your connection and try again.');
    });
  });
})();
