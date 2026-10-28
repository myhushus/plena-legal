/* Stable entry URLs resolve to current translated documents; ?choose keeps the selector. */
(function () {
  'use strict';
  var script = document.currentScript;
  var query = new URLSearchParams(window.location.search);
  if (!script || query.has('choose')) return;
  var language = (query.get('lang') || navigator.language || 'en').toLowerCase().split(/[-_]/)[0];
  if (language !== 'ko' && language !== 'es' && language !== 'fr' && language !== 'pt' && language !== 'de' && language !== 'ja') language = 'en';
  window.location.replace('/' + script.dataset.document + '/' + language + '/v' + script.dataset.version + '/' + window.location.hash);
}());
