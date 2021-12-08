function count(e, arg){
  if (arg=='img'){
    let inputImg = e.nextElementSibling.nextElementSibling.firstElementChild;
    inputImg.value ++;
  } else if (arg=='title') {
    let inputTitle = e.nextElementSibling.firstElementChild;
    inputTitle.value ++;
  } else {
    let inputMenos = e.parentElement.firstElementChild;
    inputMenos.value --;
  }
}

function range(e){
  let input = e.parentElement.parentElement.parentElement.lastElementChild.firstElementChild;
  input.value = e.value;
}
