

function addNewItem(e) {
    var addNewItem = $("#add_new_product_form");
    $.ajax({
        type: 'POST',
        url: "{% url 'servicos' opc='add item' %}",
        data: addNewItem.serialize(),
        success: function(res){
            alert(res['msg'])
        }
    })
}

function formatarCNPJ(e){

    var v= e.target.value.replace(/\D/g,"");

    v=v.replace(/^(\d{2})(\d)/,"$1.$2");
    v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3");
    v=v.replace(/\.(\d{3})(\d)/,".$1/$2");
    v=v.replace(/(\d{4})(\d)/,"$1-$2");  

    e.target.value = v;
}

function formatarCPF(e){

    var v=e.target.value.replace(/\D/g,"");

    v=v.replace(/(\d{3})(\d)/,"$1.$2");
    v=v.replace(/(\d{3})(\d)/,"$1.$2");
    v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2");

    e.target.value = v;

} 


function formatarCep(e){

    var v= e.target.value.replace(/\D/g,"")                

    v=v.replace(/^(\d{5})(\d)/,"$1-$2") 

    e.target.value = v;
        
}

function formatarTelefone(e){

    var v=e.target.value.replace(/\D/g,"");

    v=v.replace(/^(\d\d)(\d)/g,"($1)$2"); 
    v=v.replace(/(\d{5})(\d)/,"$1-$2");    

    e.target.value = v;

}

function formatarData(e){

    var v=e.target.value.replace(/\D/g,"");

    v=v.replace(/(\d{2})(\d)/,"$1/$2") 
    v=v.replace(/(\d{2})(\d)/,"$1/$2") 

    e.target.value = v;

}

function formatarMoeda(e) {

    var v = e.target.value.replace(/\D/g,"");

    v = (v/100).toFixed(2) + "";
    v = v.replace(".", ",");
    v = v.replace(/(\d)(\d{3})(\d{3}),/g, "$1.$2.$3,");
    v = v.replace(/(\d)(\d{3}),/g, "$1.$2,");

    e.target.value = v;

}

function validarTelefone(e){

    var texto = e.target.value;

    var RegExp = /^\(\d{2}\)\d{5}-\d{4}/;

    if (texto.match(RegExp) != null) {

        alert("telefone válido");

    } else {

        alert("telefone inválido");

        e.target.value = "";

    }

}