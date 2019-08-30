function whatDay() {
  var text = [
    "Or rather, Sunday",
    "Monday for sure",
    "Nope - It's Tuesday",
    "Try again. It's Wednesday",
    "And &hellip;",
    "Wrong! Try Friday",
    "S-A-T-U-R-D-A-Y Night"
  ];
  var index = new Date().getDay();
  return text[index];
}

subtitle = function() {
  var elem = document.getElementById("subtitle");
  elem.innerText = whatDay();
};
