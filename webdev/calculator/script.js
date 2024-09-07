

function toDisplay(input){
    display = document.getElementById("display");
    display.value += input;
}

function evaluateEquation(){
    try{
        const display = document.getElementById('display');
        const result = eval(display.value); // Pass the expression to evaluate as an argument
        display.value = result;
    }catch(error){
        display.value = "Error";
    }
}

