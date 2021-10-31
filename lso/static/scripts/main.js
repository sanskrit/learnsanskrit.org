/** Call a function for each text node. */
const DEFAULT_SA1 = 'devanagari';
const DEFAULT_SA2 = 'iast';
const KEY_SA1 = 'script-sa1';
const KEY_SA2 = 'script-sa2';
const MENU_SA1 = '#switch-sa1'
const MENU_SA2 = '#switch-sa2'


function forEachTextNode(elem, callback) {
  const nodeList = elem.childNodes;
  for (let i = 0; i < nodeList.length; i++) {
    const node = nodeList[i];
    if (node.nodeType === Node.TEXT_NODE) {
      node.textContent = callback(node.textContent);
    } else {
      // Ignore lang="en"
      if (node.lang !== 'en') {
        forEachTextNode(node, callback);
      }
	}
  }
}

// Get and set user data.
function getUserSa1() {
  return localStorage.getItem(KEY_SA1) || DEFAULT_SA1;
}
function setUserSa1(value) {
  localStorage.setItem(KEY_SA1, value);
}
function getUserSa2() {
  return localStorage.getItem(KEY_SA2) || DEFAULT_SA2;
}
function setUserSa2(value) {
  localStorage.setItem(KEY_SA2, value);
}


// Main transliteration function
function transliterate(src, dest, selector) {
  if (src === dest) { return };
  document.querySelectorAll(selector).forEach((elem) => {
    if (dest !== DEFAULT_SA2) {
        elem.classList.add('sa-reset');
    } else {
        elem.classList.remove('sa-reset');
    }
    forEachTextNode(elem, (s) => {
      return Sanscript.t(s.toLowerCase(), src, dest);
    });
  });
}

function switchSa1(value) {
    const oldValue = getUserSa1();
    setUserSa1(value);
    transliterate(oldValue, value, '.sa1');
}

function switchSa2(value) {
    const oldValue = getUserSa2();
    setUserSa2(value);
    transliterate(oldValue, value, '.sa2');
}

// Last JS called.
(function() {
  transliterate(DEFAULT_SA1, getUserSa1(), '.sa1');
  transliterate(DEFAULT_SA2, getUserSa2(), '.sa2');

  // Update menu to match.
  const menuSa1 = document.querySelector(MENU_SA1);
  if (menuSa1) {
    menuSa1.value = getUserSa1();
  }

  const menuSa2 = document.querySelector(MENU_SA2);
  if (menuSa1) {
    menuSa2.value = getUserSa2();
  }
})();
