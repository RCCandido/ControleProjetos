

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