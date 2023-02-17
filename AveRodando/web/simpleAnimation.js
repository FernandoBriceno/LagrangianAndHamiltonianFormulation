function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
  }

$(document).on("click",".contenedor",async function(){
    await delay(500);
    $(document.getElementById("graficas-continer")).ready(function() {
        $(document.getElementById("graficas-continer")).scrollTop($(document.getElementById("graficas-continer")).height()+100000);
    });
  })


