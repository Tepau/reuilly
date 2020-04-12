// Ajout du prix total :
let total = document.createElement("p"); //
var price = 0;
var price_cotisation = 0;
var prix_total;
var text = document.getElementById('id_nom');
var bouton = document.getElementById("total");
var valid = document.getElementById("valid");

// Gestion checkbox obligatoire
var choix_forfait = document.getElementById('id_forfait_1');
choix_forfait.required = true;


// Traitements sur des boutons radio :
$("input[type=radio][name=forfait]").change(function() {
  if($(this).val() == 'fille -11ans') {
    price_cotisation = 50;
  }else if($(this).val() == 'enfant -11ans') {
    price_cotisation = 140;
  }else if($(this).val() == 'enfant +11ans') {
    price_cotisation = 155;
  }else if($(this).val() == 'adulte competition') {
    price_cotisation = 155;
  }else if($(this).val() == 'adulte loisir') {
    price_cotisation = 145;
  }
  total.textContent = "Total"  + " = " + (price_cotisation + price).toString() + "€";
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


$("input[type=checkbox][id=id_competitions_1]").change(function() {
  if(this.checked) {
    price += 41;
    total.textContent = "Total"  + " = " + (price_cotisation + price).toString() + "€";
  }else if(!this.checked) {
    price -= 41;
    total.textContent = "Total"  + " = " + (price_cotisation + price).toString() + "€";
  }
});

$("input[type=checkbox][id=id_competitions_2]").change(function() {
  if(this.checked) {
    price += 25;
    total.textContent = "Total"  + " = " + (price_cotisation + price).toString() + "€";
  }else if(!this.checked) {
    price -= 25;
    total.textContent = "Total"  + " = " + (price_cotisation + price).toString() + "€";
  }
});



