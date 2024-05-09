// mymarkup.js

const elementArray = document.getElementsByClassName('md')

for(var i = 0; i < elementArray.length; i++) {
    var rawmd = elementArray[i].innerHTML
    elementArray[i].innerHTML = marked.parse(rawmd)
}   


