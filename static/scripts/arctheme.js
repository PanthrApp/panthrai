function get_cookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function hslToHex(h, s, l) {
  l /= 100;
  const a = s * Math.min(l, 1 - l) / 100;
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
  };
  return `#${f(0)}${f(8)}${f(4)}`;
}

document.documentElement.style.setProperty('--background-color', "#111");
document.documentElement.style.setProperty('--background-accent1', "#181818");
document.documentElement.style.setProperty('--background-accent2', "#121212");
document.documentElement.style.setProperty('--navbar-color', "#000");
document.documentElement.style.setProperty('--navbar-accent', "#111");
document.documentElement.style.setProperty('--text-color', "#fff");
document.documentElement.style.setProperty('--link-color', "#157aff");
document.documentElement.style.setProperty('--link-accent', "#569fff");
document.documentElement.style.setProperty('--navbar-link-color', "#fff");
document.documentElement.style.setProperty('--navbar-link-accent', "#ddd");

function setarctheme() {
  var hex = getComputedStyle(document.body).getPropertyValue('--arc-palette-foregroundSecondary').slice(0, 7);
  if (hex.charAt(0) !== '#') {
    return;
  }
  if (hex == "#CDB6A2") {
    document.documentElement.style.setProperty('--background-color', "#111");
    document.documentElement.style.setProperty('--background-accent1', "#181818");
    document.documentElement.style.setProperty('--background-accent2', "#121212");
    document.documentElement.style.setProperty('--navbar-color', "#000");
    document.documentElement.style.setProperty('--navbar-accent', "#111");
    document.documentElement.style.setProperty('--text-color', "#fff");
    document.documentElement.style.setProperty('--link-color', "#157aff");
    document.documentElement.style.setProperty('--link-accent', "#569fff");
    document.documentElement.style.setProperty('--navbar-link-color', "#fff");
    document.documentElement.style.setProperty('--navbar-link-accent', "#ddd");
    document.cookie = "arctheme=; path=/; max-age=31536000; samesite=strict; secure;";
    return;
  }
  document.cookie = "arctheme=" + hex + "; path=/; max-age=31536000; samesite=strict; secure;";
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  
  var r = parseInt(result[1], 16);
  var g = parseInt(result[2], 16);
  var b = parseInt(result[3], 16);
  
  r /= 255, g /= 255, b /= 255;
  var max = Math.max(r, g, b), min = Math.min(r, g, b);
  var h, s, l = (max + min) / 2;
  
  if(max == min){
    h = s = 0; // achromatic
  } else {
    var d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch(max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }
  
  s = s*100;
  s = Math.round(s);
  l = l*100;
  l = Math.round(l);
  h = Math.round(360*h);
  if (l < 65) {
    l = 70;
  }
  if (s > 80) {
    s = 75;
  }
  document.documentElement.style.setProperty('--navbar-color', hslToHex(h, s+15, l-56));
  document.documentElement.style.setProperty('--navbar-accent', hslToHex(h, s+20, l-60));
  document.documentElement.style.setProperty('--background-color', hslToHex(h, s+20, l-55));
  document.documentElement.style.setProperty('--background-accent1', hslToHex(h, s+10, l-58));
  document.documentElement.style.setProperty('--background-accent2', hslToHex(h, s+10, l-62));
  document.documentElement.style.setProperty('--text-color', hslToHex(h, s, l+15));
  document.documentElement.style.setProperty('--link-color', hslToHex(h, s+15, l));
  document.documentElement.style.setProperty('--link-accent', hslToHex(h, s+20, l-10));
  document.documentElement.style.setProperty('--navbar-link-color', hslToHex(h, s+15, l));
  document.documentElement.style.setProperty('--navbar-link-accent', hslToHex(h, s+20, l-10));
}

const cssVariableName = '--arc-palette-foregroundSecondary'; // Replace with your CSS variable name
let lastValue = getComputedStyle(document.documentElement).getPropertyValue(cssVariableName);

setInterval(() => {
  const currentValue = getComputedStyle(document.documentElement).getPropertyValue(cssVariableName);
  if (currentValue !== lastValue) {
    // console.log('CSS variable changed!');
    setarctheme();
    lastValue = currentValue;
  }
}, 50);

if (document.cookie.indexOf("arctheme=") != -1) {
  console.log("Theme cookie found");
  hex = get_cookie("arctheme");
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  
  var r = parseInt(result[1], 16);
  var g = parseInt(result[2], 16);
  var b = parseInt(result[3], 16);
  
  r /= 255, g /= 255, b /= 255;
  var max = Math.max(r, g, b), min = Math.min(r, g, b);
  var h, s, l = (max + min) / 2;
  
  if(max == min){
    h = s = 0; // achromatic
  } else {
    var d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch(max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }
  
  s = s*100;
  s = Math.round(s);
  l = l*100;
  l = Math.round(l);
  h = Math.round(360*h);
  if (l < 65) {
    l = 70;
  }
  if (s > 80) {
    s = 75;
  }
  document.documentElement.style.setProperty('--navbar-color', hslToHex(h, s+15, l-56));
  document.documentElement.style.setProperty('--navbar-accent', hslToHex(h, s+20, l-60));
  document.documentElement.style.setProperty('--background-color', hslToHex(h, s+20, l-55));
  document.documentElement.style.setProperty('--background-accent1', hslToHex(h, s+10, l-58));
  document.documentElement.style.setProperty('--background-accent2', hslToHex(h, s+10, l-62));
  document.documentElement.style.setProperty('--text-color', hslToHex(h, s, l+15));
  document.documentElement.style.setProperty('--link-color', hslToHex(h, s+15, l));
  document.documentElement.style.setProperty('--link-accent', hslToHex(h, s+20, l-10));
  document.documentElement.style.setProperty('--navbar-link-color', hslToHex(h, s+15, l));
  document.documentElement.style.setProperty('--navbar-link-accent', hslToHex(h, s+20, l-10));
}