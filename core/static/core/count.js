function count(e){
  let input = e.firstElementChild.lastElementChild.firstElementChild;
  input.value ++;
}

function range(e){
  let input = e.parentElement.parentElement.parentElement.lastElementChild.firstElementChild;
  input.value = e.value;
}
