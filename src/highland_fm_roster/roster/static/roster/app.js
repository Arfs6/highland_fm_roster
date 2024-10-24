document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM fully loaded and parsed');
  M.AutoInit();
  document.body.addEventListener('htmx:load', function(evt) {
    console.log('Event listener for htmx:load event.');
    console.log(evt.detail.elt);
    if (evt.detail.elt.classList.contains('modal')) {
      M.Modal.init([evt.detail.elt]);
      const instance = M.Modal.getInstance(evt.detail.elt);
      instance.open();
      console.log(`Modal <${evt.detail.elt.id}> opened`);
    }
  });
  htmx.onLoad(function(content) {
    console.log('called htmx.onLoad function')
    const dropdowns = content.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(dropdowns);
    console.log('Initialized dropdowns.')
  });
});
