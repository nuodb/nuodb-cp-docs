// CircleCI Artifacts does not navigate to index.html as default page which
// prevents static sides to load properly. See
// https://discuss.circleci.com/t/circle-artifacts-com-not-using-index-html/320
window.onload = function(){

  var de = document.documentElement || document.body;

  // An event listener on any element click event. We specifically detect for links and redirect the
  // outcome
  var onLinkClick = function(e,t,href){
    // Handle old versions of IE
    e = e || Event; t = e.target || e.srcElement;
    if ( t.getAttribute('href') == null ) return;
    if ( t.getAttribute('href').indexOf('../') === 0 ) return;
    if ( String(t.nodeName).toLowerCase() == 'a' ) {
      if ( e.preventDefault ) { e.preventDefault(); }
      try {
        window.location.href = appendIndexToHref(t.href)
      } catch (error) {
        console.log("Failed to modify href", href, error)
      }
      return (e.returnValue = false);
    }
  }

  // Add the listener to the body or document element, this will trigger the
  // event onclick
  if ( de.addEventListener ) {
    // Handles modern browsers
    de.addEventListener('click', onLinkClick, true);
  }
  else {
    // Handles old IE
    de.attachEvent('onclick', onLinkClick)
  }
}

function appendIndexToHref( href ){
  var uri = new URL(href)
  var self = new URL(window.location)
  if ( self.origin != uri.origin ) {
    // The href is not a local link
    return href
  }
  if ( uri.pathname.endsWith("/") ) {
    // The URI is missing a file name
    uri.pathname += "index.html"
  } else if ( !uri.includes('.') ) {
    // The URI is missing a file extension
    uri.pathname += '/index.html'
  }
  return uri.href
}
