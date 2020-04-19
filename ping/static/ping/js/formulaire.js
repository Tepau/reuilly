// Ajout du prix total :
let total = document.createElement("p"); //
var price = 0;
var price_cotisation = 0;
var prix_total;
var bouton = document.getElementById("total");
var valid = document.getElementById("valid");

// Gestion checkbox obligatoire
var choix_forfait = document.getElementsByName('forfait')[0];
choix_forfait.required = true;


// Traitements sur des boutons radio :
$("input[type=radio][name=forfait]").change(function() {
  indice_prix = $(this).val().indexOf('&');
  recup_prix = $(this).val().substr(indice_prix + 1);
  price_cotisation = parseFloat(recup_prix);
  if (price === 0) {
    prix_total = price_cotisation;
  } else {
    prix_total = price_cotisation + price;
  }
  total.textContent = "Total"  + " = " + (prix_total).toString() + "€";
  bouton.insertBefore(total, valid);
  $(function(){

    var requiredCheckboxes = $(':checkbox[required]');
    var requiredCheckboxes = $(':checkbox[required]');

    requiredCheckboxes.change(function(){

        if(requiredCheckboxes.is(':checked')) {
            requiredCheckboxes.removeAttr('required');
        }

        else {
            requiredCheckboxes.attr('required', 'required');
        }
    });
  });
});


$("input[type=checkbox]").change(function() {
  if(this.checked) {
    indice_prix = $(this).val().indexOf('&');
    recup_prix = $(this).val().substr(indice_prix + 1);
    price += parseFloat(recup_prix);
    if (price_cotisation === 0){
      prix_total = price;
    } else {
      prix_total = price_cotisation + price;
    }
    total.textContent = "Total"  + " = " + (prix_total).toString() + "€";
    bouton.insertBefore(total, valid);
  }else if(!this.checked){
    indice_prix = $(this).val().indexOf('&');
    recup_prix = $(this).val().substr(indice_prix + 1);
    price -= parseFloat(recup_prix);
    if ((price === 0) && (price_cotisation === 0)) {
      prix_total = 0;
    } else if ((price ===0) && (price_cotisation > 0)) {
      prix_total = price_cotisation;
    } else if ((price > 0) && (price_cotisation === 0)){
      prix_total = price;
    } else {
      prix_total = price + price_cotisation;
    }
    total.textContent = "Total"  + " = " + (prix_total).toString() + "€";
  }

});


